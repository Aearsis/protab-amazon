from django.db import models

from team.models import Player


class Channel(models.Model):
    players = models.ManyToManyField(Player)

    @classmethod
    def create(cls, *players):
        c = Channel()
        c.save()
        for p in players:
            c.players.add(p)
        return c

    def __str__(self):
        return "Channel: {} msgs, {}".format(self.message_set.count(), ",".join(str(p) for p in self.players.all()))


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT)
    author = models.ForeignKey(Player, on_delete=models.PROTECT)
    content = models.TextField()
