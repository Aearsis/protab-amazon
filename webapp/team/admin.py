from django.contrib import admin

from team.models import Player, Team, PlayerMenuItem

admin.site.register(Player)
admin.site.register(PlayerMenuItem)
admin.site.register(Team)

