from django.contrib import admin

from chat.models import Channel, Message

admin.site.register(Channel)
admin.site.register(Message)
