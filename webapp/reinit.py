#!/usr/bin/env python

import random

from django.urls import reverse

from webapp import wsgi

from django.contrib.auth.models import Permission, User, Group
from django.db import transaction

from chat.models import Message, Channel
from goods.models import Goods, GoodsType, SellSlot
from team.models import Player, Team, PlayerMenuItem
from webapp.settings import DEBUG, SELL_SLOTS
from webapp.utils import random_token

foo = wsgi.application
random.seed(42)


def clean_all():
    for model in (Message, Channel, PlayerMenuItem, SellSlot, Player, Team):
        model.objects.all().delete()

    User.objects.filter(username__startswith='player').delete()


def create_channel(*players):
    c = Channel()
    c.save()
    ps = set(players)
    for p in players:
        c.players.add(p)
        menuitem = PlayerMenuItem()
        menuitem.player = p
        menuitem.label = "Chat s {}".format(" a ".join(pp.instr.lower() for pp in ps - {p}))
        menuitem.url = reverse('channel', args=[c.pk])
        menuitem.save()

    return c


def create_player(team: Team, role: str, name: str, instr: str):
    p = Player()
    p.login_token = random_token(10)
    p.team = team
    p.name = name
    p.instr = instr

    username = 'player_{}_{}'.format(team.pk, role.lower())
    u = p.user = User.objects.create_user(username, username + '@protab.cz', p.login_token)
    u.last_name = team.name
    u.first_name = name
    u.save()

    p.save()
    print("\t{}: {}".format(name, p.login_token))
    return p


def init_teams(count):
    mine_group = Group.objects.get(name='Miners')
    sell_group = Group.objects.get(name='Sellers')

    for i in range(count):
        t = Team(i)
        t.name = "Tým {}".format(i + 1)
        t.save()
        print(t.name)

        miner = create_player(t, "Továrník", "Továrníci", "továrníky")
        broker = create_player(t, "Broker", "Obchodní manažeři", "obchodními manažery")
        seller = create_player(t, "Seller", "Prodavači", "prodavači")

        for i in range(SELL_SLOTS):
            SellSlot.create_for(seller)

        miner.user.groups.add(mine_group)
        seller.user.groups.add(sell_group)

        miner.save()
        seller.save()

        create_channel(broker, miner)
        create_channel(broker, seller)

    if DEBUG:
        t = Team(42)
        t.name = "Orgtým - DEBUG :)"
        t.save()

        p = Player()
        p.user = User.objects.get(username='aearsis')
        p.name = "Orgové"
        p.team = t
        p.instr = "Orgy"
        p.save()
        for i in range(SELL_SLOTS):
            SellSlot.create_for(p)


def init_goods(count):
    for gt in GoodsType.objects.all():
        for _ in range(count):
            g = Goods()
            g.type = gt
            g.token = random_token(Goods.TOKEN_LEN)
            g.save()


@transaction.atomic
def initialize():
    clean_all()
    init_teams(4)
    #init_goods(300)


if __name__ == '__main__':
    initialize()
