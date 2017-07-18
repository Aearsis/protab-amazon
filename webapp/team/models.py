from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


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

    # Oh yeah, we store the "password" for players in plaintext.
    login_token = models.CharField(max_length=TOKEN_LEN)

    user = models.OneToOneField(User)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    # Name for the purpose of chatting
    name = models.TextField()
    # Name in instrumental
    instr = models.TextField()

    def __str__(self):
        return "{} / {}".format(self.team, self.user.first_name)


class PlayerMenuItem(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    label = models.CharField(max_length=64)
    url = models.CharField(max_length=128)
