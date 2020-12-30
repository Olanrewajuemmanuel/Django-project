from django.db import models
from django.utils import timezone


# Create your models here.

class Product(models.Model):
    item_name = models.TextField(max_length=120, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    stock_amount = models.IntegerField(blank=False)
    featured = models.BooleanField(default=False)
    amount_sold = models.IntegerField(default=0)
    company = models.TextField(max_length=120)
    image = models.ImageField(upload_to='pictures', max_length=None)

    def top_selling(self):
        return self.amount_sold >= 100

    def __str__(self):
        return self.item_name


class Users(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(blank=True, max_length=14)
    password = models.CharField(max_length=255)
    time_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
