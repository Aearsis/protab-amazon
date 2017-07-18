from django.contrib import admin
from django.contrib.admin import ModelAdmin

from chat.models import Channel
from goods.models import Goods, GoodsType
from team.models import Team

admin.site.register(GoodsType)


@admin.register(Goods)
class GoodsAdmin(ModelAdmin):
    list_display = ('type', 'token', 'mined_at', 'owner', 'sold_at', 'sold_for')
