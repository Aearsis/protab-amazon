from django import forms
from django.forms import Form

from team.models import Player


class TokenAuthenticationForm(Form):
    token = forms.CharField(min_length=Player.TOKEN_LEN, max_length=Player.TOKEN_LEN, label="Přihlašovací token",
                            widget=forms.TextInput(attrs={'autofocus': True}))
    error_messages = {
        'invalid_login': "Token je nesprávný."
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(TokenAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        token = self.cleaned_data.get('token')
        player = Player.objects.filter(login_token=token).first()
        if player is None:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )
        self.user_cache = player.user

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
