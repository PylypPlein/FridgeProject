from django.db import models
from django.contrib.auth.models import User

class AbstractProduct(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    expiration_date = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Product(AbstractProduct):
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField(null=True, blank=True)

class Fridge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    capacity = models.FloatField()  # Capacity of the fridge in liters
    products = models.ManyToManyField(Product, related_name='fridges', through='FridgeProduct')

    def __str__(self):
        return f"{self.user.username}'s {self.name}"

class FridgeProduct(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} {self.product.name}(s) in {self.fridge.name}"
