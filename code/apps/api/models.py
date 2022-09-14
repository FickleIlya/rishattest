from django.db import models
from django.db.models import Max


class Order(models.Model):
    order_id = models.CharField(primary_key=True, editable=False, max_length=10)

    def save(self, **kwargs):
        if not self.order_id:
            max = Order.objects.aggregate(id_max=Max('order_id'))['id_max']
            self.id = "{}{:05d}".format('N', max if max is not None else 1)
        super().save(*kwargs)


class Item(models.Model):
    name = models.TextField()
    description = models.TextField()
    price = models.TextField()
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)

