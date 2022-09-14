from django.db import models


class Item(models.Model):
    name = models.TextField()
    description = models.TextField()
    price = models.TextField()
