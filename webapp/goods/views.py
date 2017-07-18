from django.contrib import messages
from django.db.models import *
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from goods.forms import TokenForm
from goods.models import Goods, GoodsType
from webapp.utils import miner_required


@method_decorator(miner_required, name='dispatch')
class MineView(FormView):
    form_class = TokenForm
    template_name = 'goods/mine.html'

    def form_valid(self, form):
        try:
            g = Goods.mine(self.request.team, form.cleaned_data['code'].upper())
            if g is not None:
                messages.add_message(self.request, messages.SUCCESS, "Získali jste {}!".format(g.type))
            else:
                messages.add_message(self.request, messages.INFO, "Takový lísteček neexistuje!")
        except Goods.InvalidStateTransition:
            messages.add_message(self.request, messages.INFO, "Takový lísteček neexistuje!")
        return redirect("mine")


@method_decorator(miner_required, name='dispatch')
class StorageView(TemplateView):
    template_name = 'goods/storage.html'

    def get_context_data(self, **kwargs):
        context = super(StorageView, self).get_context_data(**kwargs)
        context['storage'] = GoodsType.objects.all().annotate(
            mined_count=Sum(Case(
                When(goods__owner=self.request.team, goods__sold_at__isnull=True, then=1),
                default=0,
                output_field=IntegerField())),
            sold_count=Sum(Case(
                When(goods__owner=self.request.team, goods__sold_at__isnull=False, then=1),
                default=0,
                output_field=IntegerField())),
            earn=Sum(Case(
                When(goods__owner=self.request.team, goods__sold_at__isnull=False, then='goods__sold_for'),
                default=0,
                output_field=FloatField()))
        )
        return context
