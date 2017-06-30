from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden

from team.forms import TokenAuthenticationForm


class TokenLoginView(LoginView):
    form_class = TokenAuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(TokenLoginView, self).dispatch(request, *args, **kwargs)


