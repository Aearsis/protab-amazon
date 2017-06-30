from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from goods.forms import TokenForm
from goods.models import Goods
from webapp.utils import miner_required


@method_decorator(miner_required, name='dispatch')
class MineView(FormView):
    form_class = TokenForm
    template_name = 'goods/mine.html'

    def form_valid(self, form):
        try:
            g = Goods.mine(self.request.team, form.cleaned_data['code'])
            if g is not None:
                messages.add_message(self.request, messages.SUCCESS, "Našel jsi {}!".format(g.type))
            else:
                messages.add_message(self.request, messages.INFO, "Takový lísteček neexistuje!")
            return redirect("token:input")
        except Goods.InvalidStateTransition:
            return HttpResponseForbidden()
