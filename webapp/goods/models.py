from datetime import timedelta

import sys
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_naive

from team.models import Team, Player

sys.path.append('..')
from data import get_stock_value


class GoodsType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Selling information
    sell_quest = models.TextField()
    # The quest must take at least this much seconds
    sell_time_sec = models.IntegerField()

    def __str__(self):
        return self.name

    def get_price(self, sold_at: datetime):
        return get_stock_value(self.pk - 1, make_naive(sold_at))


class Goods(models.Model):
    TOKEN_LEN = 8
    type = models.ForeignKey(GoodsType)

    # Phase one: no owner
    token = models.CharField(max_length=TOKEN_LEN, primary_key=True)

    # Phase two: owning team
    mined_at = models.DateTimeField(null=True, default=None)
    owner = models.ForeignKey(Team, null=True, default=None)

    # Phase three: sold
    sold_at = models.DateTimeField(null=True, default=None)
    sold_for = models.FloatField(null=True, default=None)  # Cached price the goods were sold for

    def __str__(self):
        return "{} ({}) - {}".format(self.type, self.token, self.get_state())

    def get_state(self):
        if self.sold_at is not None:
            return 'sold'
        elif self.owner is not None:
            return 'mined'
        else:
            return 'free'

    class Meta:
        permissions = (
            ('goods.can_mine', 'Insert tokens'),
            ('goods.can_sell', 'Sell goods')
        )

        verbose_name_plural = "Goods"

    @classmethod
    @transaction.atomic
    def mine(cls, team: Team, code: str):
        g = cls.objects.filter(token=code).first()
        if g is None:
            return None

        if g.owner is not None:
            raise Goods.InvalidStateTransition(g)

        g.mined_at = timezone.now()
        g.owner = team
        g.save()
        return g

    class InvalidStateTransition(Exception):
        pass


class SellSlot(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    selling = models.ForeignKey(GoodsType, null=True)
    started_at = models.DateTimeField(null=True)

    def get_min_finish_time(self):
        duration = timedelta(seconds=self.selling.sell_time_sec)
        return self.started_at + duration

    def start_selling(self, goods_type: GoodsType):
        self.selling = goods_type
        self.started_at = timezone.now()
        self.save()

    @transaction.atomic
    def finish_selling(self):
        if self.selling is None:
            raise PermissionDenied("You must stat selling first.")
        if timezone.now() < self.get_min_finish_time():
            raise PermissionDenied("To jsi nemohl stihnout.")

        g = Goods.objects.filter(type=self.selling, owner=self.player.team, mined_at__lte=self.started_at, sold_at=None).first()
        if g is not None:
            g.sold_at = self.started_at
            g.sold_for = self.selling.get_price(self.started_at)
            g.save()

        self.selling = None
        self.save()

    def abort_selling(self):
        self.selling = None
        self.save()

    def is_free(self):
        return self.selling is None

    @classmethod
    def create_for(cls, seller):
        slot = cls()
        slot.player = seller
        slot.selling = None
        slot.save()

    class Meta:
        ordering = ['pk']

