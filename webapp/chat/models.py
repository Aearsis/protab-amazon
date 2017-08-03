from datetime import timedelta, datetime

from django.db import models
from django.db.models import Q
from django.urls import resolve, reverse
from django.utils import timezone

from team.models import Player, PlayerMenuItem


class Channel(models.Model):
    players = models.ManyToManyField(Player)

    # The messages are queued through leaky bucket. The minimal delay is MAX_REFRESH_PERIOD,
    # and at most one message per MIN_MESSAGE_PERIOD is sent.
    MAX_REFRESH_PERIOD = timedelta(seconds=3)
    MIN_MESSAGE_PERIOD = timedelta(seconds=60)

    class Meta:
        permissions = (
            ('channel.admin', 'View all channels, send without delay'),
        )

    def __str__(self):
        return "Channel: {} msgs, {}".format(self.message_set.count(), ", ".join(str(p) for p in self.players.all()))

    def get_next_refresh_time(self) -> timedelta:
        try:
            first_msg = self.message_set.filter(visible__gt=timezone.now())[0]
            to_first_msg = first_msg.visible - timezone.now()
            return min(to_first_msg, Channel.MAX_REFRESH_PERIOD)
        except IndexError:
            return Channel.MAX_REFRESH_PERIOD

    def get_visible_messages(self, for_player):
        return self.message_set.filter(Q(visible__lte=timezone.now()) | Q(author=for_player))

    def get_next_visible_time(self, message) -> datetime:
        if message.author.user.has_perm('channel.admin'):
            return timezone.now()
        try:
            last_visible = self.message_set.filter(author=message.author).order_by('-visible')[0].visible
            after_last_msg = last_visible + Channel.MIN_MESSAGE_PERIOD

            typing_delay = last_visible + ((len(message.content) / 300) * timedelta(seconds=1))
            return max(after_last_msg, typing_delay, timezone.now() + Channel.MAX_REFRESH_PERIOD)
        except IndexError:
            return timezone.now() + Channel.MAX_REFRESH_PERIOD

    def post(self, author, content):
        msg = Message()
        msg.author = author
        msg.channel = self
        msg.posted = timezone.now()
        msg.content = content
        msg.visible = self.get_next_visible_time(msg)
        return msg.save()


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT)
    author = models.ForeignKey(Player, on_delete=models.PROTECT)
    posted = models.DateTimeField()
    visible = models.DateTimeField()
    content = models.TextField()

    class Meta:
        ordering = ['posted']

    def is_visible(self):
        return self.visible <= timezone.now()
