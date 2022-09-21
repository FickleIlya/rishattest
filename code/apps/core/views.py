import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView

from .models import Item, Order


# Create your views here.
class ViewItems(ListView):
    model = Item
    template_name = "all_items.html"
    context_object_name = "items"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Item.objects.all()


class ViewOrder(TemplateView):
    model = Order
    template_name = "order_info.html"

    def get_context_data(self, **kwargs):
        order = Order.objects.get(order_id=self.kwargs.get("order_id")).items.all()
        total = sum([int(item.price) for item in order]) / 100

        context = super().get_context_data(**kwargs)
        context["order_id"] = self.kwargs.get("order_id")
        context["order"] = order
        context["total"] = total
        return context


class ViewItemDetail(ListView):
    model = Item
    template_name = "item_info.html"
    context_object_name = "item"

    def get_queryset(self):
        return Item.objects.get(id=self.kwargs.get("item_id"))


class GetOrderId(View):

    def get(self, request, *args, **kwargs):
        request = self.request.GET
        order_id = requests.post(f'https://fickle-rishattest.tk/api/v1/order', data=request).json()["order_id"]
        url = reverse('core:order_info', kwargs={'order_id': order_id})

        return HttpResponseRedirect(url)
