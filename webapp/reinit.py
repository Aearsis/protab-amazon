#!/usr/bin/env python

import random

from webapp import wsgi

from django.contrib.auth.models import Permission, User
from django.db import transaction

from chat.models import Message, Channel
from goods.models import Goods, GoodsType
from team.models import Player, Team
from webapp.utils import random_token

foo = wsgi.application
random.seed(42)

def clean_all():
    for model in (Message, Channel, Goods, GoodsType, Player, Team):
        model.objects.all().delete()

    User.objects.filter(username__startswith='player').delete()


def create_player(team: Team, name: str):
    p = Player()
    p.login_token = random_token(10)
    username = 'player_' + p.login_token
    p.team = team
    u = p.user = User.objects.create_user(username, username + '@protab.cz', p.login_token)
    u.last_name = team.name
    u.first_name = name
    u.save()
    p.save()
    print("\t{}: {}".format(name, p.login_token))
    return p

def init_teams(count):
    mine_perm = Permission.objects.get(codename='goods.can_mine')
    sell_perm = Permission.objects.get(codename='goods.can_sell')

    for i in range(count):
        t = Team(i)
        t.name = "Tým {}".format(i + 1)
        t.save()
        print(t.name)

        miner = create_player(t, "Miner")
        broker = create_player(t, "Broker")
        seller = create_player(t, "Seller")

        miner.user.user_permissions.add(mine_perm)
        seller.user.user_permissions.add(sell_perm)

        Channel.create(broker, miner)
        Channel.create(broker, seller)


def init_goods(count):
    for type in ["Mikroprocesory", "Tučňáci", "Okýnka"]:
        gt = GoodsType()
        gt.name = type
        gt.save()

        for _ in range(count):
            g = Goods()
            g.type = gt
            g.token = random_token(Goods.TOKEN_LEN)
            g.save()


@transaction.atomic
def initialize():
    clean_all()
    init_teams(4)
    init_goods(10)

if __name__ == '__main__':
    initialize()
