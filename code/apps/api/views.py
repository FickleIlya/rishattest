import os

from django.http import HttpResponse, HttpResponseRedirect
import stripe
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, Order

stripe.api_key = os.environ["API_KEY"]


class GetAllItems(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        items = Item.objects.all()
        response = {
            "items": [{
                "name": item.name,
                "description": item.description,
                "price": item.price
            } for item in items]
        }
        return Response({"items": items}, template_name="all_items.html")


class GetOrder(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        # TODO
        order = Order.objects.create()
        return Response(self.request.query_params.getlist())


class GetItem(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, item_id):

        item = Item.objects.filter(id=item_id)[0]
        if item:
            context = {
                "item": item,
            }
            return Response(context, template_name="item_info.html")
        return HttpResponse(status=404, content="Item not found")


class BuyItem(APIView):

    def get(self, request, item_id):

        item = Item.objects.filter(id=item_id)[0]
        product = stripe.Product.create(
            name=item.name,
            description=item.description
        )
        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(item.price),
            currency='usd'
        )
        session = stripe.checkout.Session.create(
            mode='payment',
            success_url='http://127.0.0.1:8000/api/v1/success',
            cancel_url='http://127.0.0.1:8000/api/v1/cancel',
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ]
        )
        return HttpResponseRedirect(session.url, status=303)


class BuyOrder(APIView):
    def get(self, request, order_id):
        order = Order.objects.get(order_id=order_id)
        price_list = []
        for item in order.item_set.all():
            product = stripe.Product.create(
                name=item.name,
                description=item.description
            )
            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(item.price),
                currency='usd'
            )
            price_list.append({'price': price.id, 'quantity': 1})

        session = stripe.checkout.Session.create(
            mode='payment',
            success_url='http://127.0.0.1:8000/api/v1/success',
            cancel_url='http://127.0.0.1:8000/api/v1/cancel',
            line_items=price_list
        )
        return HttpResponseRedirect(session.url, status=303)


class SuccessUrl(APIView):

    def get(self, request):
        return Response("success")


class CancelUrl(APIView):

    def get(self, request):
        return Response("canceled")
