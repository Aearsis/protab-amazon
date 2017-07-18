from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView

from team.forms import TokenAuthenticationForm
from team.models import Team


class TokenLoginView(LoginView):
    form_class = TokenAuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(TokenLoginView, self).dispatch(request, *args, **kwargs)


class ScoreView(TemplateView):
    template_name = "score.html"

    def get_context_data(self, **kwargs):
        context = super(ScoreView, self).get_context_data(**kwargs)
        context['score'] = Team.get_score_table()
        return context
