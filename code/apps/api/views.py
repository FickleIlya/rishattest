import os

import shortuuid
import stripe
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ItemSerializer, OrderSerializer

from core.models import Item, Order

stripe.api_key = os.environ["API_KEY"]


class GetAllItems(APIView):

    def get(self, request):
        items = Item.objects.all()
        if items:
            response = {
                "items": [{
                    "id": item.pk,
                    "name": item.name,
                    "description": item.description,
                    "price": item.price
                } for item in items]
            }
            return Response(response)
        return HttpResponse(status=404, content="Items not found")


class OrderCreateAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        items = self.request.data
        if items:
            order_id = shortuuid.uuid()
            order = Order.objects.create(order_id=order_id)
            for item_id in items:
                if item_id != 'csrfmiddlewaretoken':
                    item = Item.objects.get(id=item_id)
                    order.items.add(item)

            return Response({"order_id": order.order_id})
        return HttpResponse(status=404, content="Items is empty")


class OrderAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
        except:
            return HttpResponse(status=404, content="Order not found")
        else:
            response = OrderSerializer(order).data
            return Response(response)

    def post(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
        except:
            return HttpResponse(status=404, content="Order not found")
        else:
            price_list = []
            if items := order.items.all():
                for item in items:
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
            return HttpResponse(status=404, content="Order is empty")


class GetItem(APIView):

    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except:
            return HttpResponse(status=404, content="Item not found")
        else:
            response = ItemSerializer(item)
            return Response(response.data)

    def post(self, request, item_id):

        try:
            item = Item.objects.get(id=item_id)
        except:
            data = request.data
            item = Item.objects.create(id=item_id,
                                       name=data["name"],
                                       description=data["description"],
                                       price=data["price"])
            data["id"] = item_id
            return Response(data, status=201)
        else:
            return HttpResponse(status=404, content="Id already taken")

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except:
            return HttpResponse(status=404, content="Item not found")
        else:
            item.delete()
            return Response(status=204)

    def put(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except:
            return HttpResponse(status=404, content="Item not found")
        else:
            data = request.data
            item.name = data["name"]
            item.description = data["description"]
            item.price = data["price"]
            item.save()

            data["id"] = item_id
            return Response(data, status=200)


class BuyItem(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, item_id):
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
                cancel_url=f'https://{os.environ["ALLOWED_HOSTS"].split()[0]}/api/v1/cancel',
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
