from django.db import models
from django.db.models import Max


class Order(models.Model):
    order_id = models.CharField(primary_key=True, editable=False, max_length=22)


class Item(models.Model):
    name = models.TextField()
    description = models.TextField()
    price = models.TextField()
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)

