import os

from django.http import HttpResponse, HttpResponseRedirect
import stripe
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item

stripe.api_key = os.environ["API_KEY"]


class GetItem(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, item_id):

        item = Item.objects.filter(id=item_id)[0]
        if item:
            return Response({"item": item}, template_name="base_template.html")
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


class SuccessUlr(APIView):

    def get(self, request):
        return Response("success")


class CancelUrl(APIView):

    def get(self, request):
        return Response("canceled")
