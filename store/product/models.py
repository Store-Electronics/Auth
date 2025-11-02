from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    price_business = models.FloatField(default=0)
    stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    def __str__(self):
        return self.name
