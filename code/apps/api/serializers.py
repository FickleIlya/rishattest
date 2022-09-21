from rest_framework import serializers

from core.models import Item, Order


class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Item
        fields = ["id", "name", "description", "price"]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
