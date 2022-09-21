from django.db import models


class Item(models.Model):
    name = models.TextField()
    description = models.TextField()
    price = models.TextField()


class Order(models.Model):
    order_id = models.CharField(primary_key=True, editable=False, max_length=22)
    items = models.ManyToManyField(Item)


