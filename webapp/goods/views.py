from datetime import timedelta, datetime

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import *
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView

from goods.forms import TokenForm
from goods.models import Goods, GoodsType, SellSlot
from webapp.utils import miner_required, seller_required


class SellSlotMixin(View):
    def get_slot_context(self, slot):
        return self.request.player.sellslot_set.all()[slot]


@method_decorator(seller_required, name='dispatch')
class MarketView(SellSlotMixin, TemplateView):
    """ The overview of selling slots. Displays current state of slots. """
    template_name = 'sell.html'

    def get_context_data(self, **kwargs):
        context = super(MarketView, self).get_context_data(**kwargs)
        context['slots'] = self.request.player.sellslot_set.all()
        context['types'] = GoodsType.objects.all()
        return context


@method_decorator(seller_required, name='dispatch')
class SellView(SellSlotMixin, View):
    def get(self, request, *args, **kwargs):
        slot = get_object_or_404(SellSlot, player=request.player, pk=args[0])
        type = get_object_or_404(GoodsType, pk=args[1])
        slot.start_selling(type)
        return redirect('market')


@method_decorator(seller_required, name='dispatch')
class FinishQuestView(SellSlotMixin, View):
    def get(self, request, *args, **kwargs):
        slot = get_object_or_404(SellSlot, player=request.player, pk=args[0])
        slot.finish_selling()
        return redirect('market')


@method_decorator(seller_required, name='dispatch')
class AbortQuestView(SellSlotMixin, View):
    def get(self, request, *args, **kwargs):
        slot = get_object_or_404(SellSlot, player=request.player, pk=args[0])
        slot.abort_selling()
        return redirect('market')


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
                output_field=IntegerField()))
            ,
            earn=Sum(Case(
                When(goods__owner=self.request.team, goods__sold_at__isnull=False, then='goods__sold_for'),
                default=0,
                output_field=FloatField()))
        )
        return context


class TokensView(TemplateView):
    template_name = 'goods/tokens.html'

    def get_context_data(self, **kwargs):
        context = super(TokensView, self).get_context_data(**kwargs)
        context['goods'] = Goods.objects.all()
        return context
