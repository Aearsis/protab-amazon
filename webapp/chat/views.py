from django.core.exceptions import PermissionDenied
from django.forms import Form, CharField, Textarea
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, TemplateView
from django.views.generic.base import ContextMixin

from chat.models import Channel


class PostMessageForm(Form):
    content = CharField(widget=Textarea, label=None)


class ChannelMixin(ContextMixin, View):
    def get_channel(self) -> Channel:
        c = get_object_or_404(Channel, id=self.args[0])
        if self.request.player not in c.players.all() and not self.request.user.has_perm('channel', 'view_all'):
            raise PermissionDenied("You're not a member of this channel.")
        return c

    def get_messages(self, **kwargs):
        return [{
            'author': m.author,
            'posted': m.posted,
            'hidden': not m.is_visible(),
            'myself': m.author == self.request.player,
            'delivered': m.visible,
            'content': m.content,
        } for m in self.get_channel().get_visible_messages(self.request.player)]

    def get_context_data(self, **kwargs):
        context = super(ChannelMixin, self).get_context_data(**kwargs)
        context['visible_messages'] = self.get_messages()
        context['refresh_after'] = self.get_refresh_sec()
        return context

    def get_refresh_sec(self):
        return self.get_channel().get_next_refresh_time().total_seconds()


class MessagesView(ChannelMixin, TemplateView):
    template_name = 'bits/channel.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response['X-Refresh-After'] = self.get_refresh_sec()
        return response


class ChannelView(ChannelMixin, FormView):
    form_class = PostMessageForm
    template_name = 'channel.html'

    def form_valid(self, form):
        channel = self.get_channel()
        channel.post(self.request.player, form.cleaned_data['content'])
        return redirect("channel", channel.pk)
