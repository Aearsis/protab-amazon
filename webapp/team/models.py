from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from webapp.utils import random_token


class Team(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="Název týmu")
    members = models.TextField(verbose_name="Seznam členů")

    def __str__(self):
        return self.name

    def get_score(self):
        return self.goods_set.filter(sold_for__isnull=False).aggregate(Sum('sold_for'))

    @classmethod
    def get_score_table(cls):
        return cls.objects.all().annotate(score=Sum('goods__sold_for'))


class Player(models.Model):
    TOKEN_LEN = 10

    # Oh yeah, we store the password for players in plaintext.
    login_token = models.CharField(max_length=TOKEN_LEN)

    user = models.OneToOneField(User)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    @classmethod

    def __str__(self):
        return self.user.first_name + "/" + str(self.team)
