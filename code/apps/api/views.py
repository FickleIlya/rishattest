import os

import shortuuid
from django.http import HttpResponse, HttpResponseRedirect
import stripe
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, Order

stripe.api_key = os.environ["API_KEY"]


class GetAllItems(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        items = Item.objects.all()
        order_id = shortuuid.uuid()
        if items:
            response = {
                "items": [{
                    "name": item.name,
                    "description": item.description,
                    "price": item.price
                } for item in items]
            }
            return Response({"items": items, "order_id": order_id}, template_name="all_items.html")
        return HttpResponse(status=404, content="Items not found")


class OrderCreateAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        order_id = shortuuid.uuid()
        order = Order.objects.create(order_id=order_id)
        items = request.data
        for item_id in items:
            if item_id != 'csrfmiddlewaretoken':
                item = Item.objects.get(id=item_id)
                order.item_set.add(item, bulk=False)

        return HttpResponseRedirect(order_id)


class OrderAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, order_id):
        order = Order.objects.get(order_id=order_id)
        items = order.item_set.all()

        total = sum([int(item.price) for item in items])/100
        return Response({"order_id": order_id, "order": order.item_set.all(), "total": total},
                        template_name="order_info.html")

    def post(self, request, order_id):
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
            success_url=f'https://{os.environ["ALLOWED_HOSTS"].split()[0]}/api/v1/success',
            cancel_url=f'http://{os.environ["ALLOWED_HOSTS"].split()[0]}/api/v1/cancel',
            line_items=price_list
            )
        return HttpResponseRedirect(session.url, status=303)


class GetItem(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except:
            return HttpResponse(status=404, content="Item not found")
        else:
            context = {
                "item": item,
                "item_id": item_id

            }
            return Response(context, template_name="item_info.html")


class BuyItem(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except:
            return HttpResponse(status=404, content="Item not found")
        else:
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
                success_url=f'https://{os.environ["ALLOWED_HOSTS"].split()[0]}/api/v1/success',
                cancel_url=f'http://{os.environ["ALLOWED_HOSTS"].split()[0]}/api/v1/cancel',
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    },
                ]
            )
            return HttpResponseRedirect(session.url, status=303)


class SuccessUrl(APIView):

    def get(self, request):
        return Response("success")


class CancelUrl(APIView):

    def get(self, request):
        return Response("canceled")
