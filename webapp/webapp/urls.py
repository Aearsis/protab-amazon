"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

from chat.views import *
from goods.views import *
from team.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', TokenLoginView.as_view(), name='login'),
    #url(r'^tokens-print-em-all/$', TokensView.as_view(), name='tokens-print'),
    url(r'^logout/$', LogoutView.as_view(template_name='logout.html'), name='logout'),
    url(r'^mine/$', MineView.as_view(), name='mine'),
    url(r'^storage/$', StorageView.as_view(), name='storage'),
    url(r'^market/$', MarketView.as_view(), name='market'),
    url(r'^sell/([0-9]+)/start-([0-9]+)$', SellView.as_view(), name='sell'),
    url(r'^sell/([0-9]+)/abort$', AbortQuestView.as_view(), name='abort-quest'),
    url(r'^sell/([0-9]+)/finish$', FinishQuestView.as_view(), name='finish-quest'),
    url(r'^scoreboard/$', ScoreView.as_view(), name='score'),
    url(r'^channel/([0-9]+)$', ChannelView.as_view(), name='channel'),

    url(r'^ajax/scoreboard/$', AjaxScoreView.as_view(), name='ajax-score'),
    url(r'^ajax/channel/([0-9]+)$', MessagesView.as_view(), name='ajax-channel'),

    url(r'^$', login_required(TemplateView.as_view(template_name='homepage.html')), name='homepage'),
]
