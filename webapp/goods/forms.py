from django import forms

from goods.models import Goods


class TokenForm(forms.Form):
    code = forms.CharField(min_length=Goods.TOKEN_LEN, max_length=Goods.TOKEN_LEN, label="Kód lístečku:",
                           widget=forms.TextInput(attrs={'autofocus':True}))