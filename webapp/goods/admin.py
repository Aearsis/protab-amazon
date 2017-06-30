from django.contrib import admin

from chat.models import Channel
from goods.models import Goods, GoodsType
from team.models import Team

admin.site.register(GoodsType)
admin.site.register(Goods)

