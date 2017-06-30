from django.db import models, transaction
from django.utils.datetime_safe import datetime

from team.models import Team


class GoodsType(models.Model):
    type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_price(self, sold_at: datetime):
        return 42
        pass


class Goods(models.Model):
    TOKEN_LEN = 8
    type = models.ForeignKey(GoodsType)

    # Phase one: no owner
    token = models.CharField(6, max_length=TOKEN_LEN, primary_key=True)

    # Phase two: owning team
    mined_time = models.DateField(null=True, default=None)
    owner = models.ForeignKey(Team, null=True, default=None)

    # Phase three: sold
    sold_at = models.DateField(null=True, default=None)
    sold_for = models.IntegerField(null=True, default=None)  # Cached price the goods were sold for

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

        g.mined_time = datetime.now()
        g.owner = team
        g.save()

    @classmethod
    @transaction.atomic
    def sell(cls, team: Team, type: GoodsType):
        g = cls.objects.filter(type=type, owner=team, sold_at=None).first()
        if g is None:
            return g

        g.sold_at = datetime.now()
        g.sold_for = type.get_price(g.sold_at)
        g.save()

    class InvalidStateTransition(Exception):
        pass

