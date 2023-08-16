from django.contrib.auth.models import AbstractUser
from django.db import models
import mongoengine

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # Add other fields for user roles and profile

    def __str__(self):
        return self.username

#from CasaLeiloes.settings import MONGOENGINE

# Create your models here.

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # Add other fields for user roles and profile

    def __str__(self):
        return self.username
#from CasaLeiloes.settings import MONGOENGINE

# Create your models here.
class Lots(models.Model):
    lot_id = models.AutoField(primary_key=True)
    lot_name = models.CharField(max_length=50)
    description = models.TextField()

class Products(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='item_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lots, on_delete=models.CASCADE)

class Auctions(models.Model):
    auction_id = models.BigAutoField(primary_key=True, default=int)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    number_of_bids = models.IntegerField()
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    minimum_increment = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)

class Negotiations(models.Model):
    negotiation_id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    number_of_bids = models.IntegerField()
    proposed_value = models.DecimalField(max_digits=6, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Watchlist(models.Model):
    watchlist_id = models.BigAutoField(primary_key=True, default=int)
    auctions = models.ManyToManyField(Auctions, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    negotiations = models.ManyToManyField(Negotiations, on_delete=models.CASCADE)

class Bids_Auction(models.Model):
    bid_id = models.IntegerField(primary_key=True, serialize=True, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()
    minimum_value = models.DecimalField(max_digits=6, decimal_places=2)
    final_value = models.DecimalField(max_digits=6, decimal_places=2)

class Bids_Negotiation(models.Model):
    bid_id = models.IntegerField(primary_key=True, serialize=True, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    negotiation = models.ForeignKey(Negotiations, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()
    minimum_value = models.DecimalField(max_digits=6, decimal_places=2)
    final_value = models.DecimalField(max_digits=6, decimal_places=2)

class CostCenter_Negotiations(models.Model):
    cost_center_id = models.AutoField(primary_key=True)
    cost_center_date = models.DateField()
    bid = models.ForeignKey(Bids_Negotiation, on_delete=models.CASCADE)

class CostCenter_Auctions(models.Model):
    cost_center_id = models.AutoField(primary_key=True)
    cost_center_date = models.DateField()
    bid = models.ForeignKey(Bids_Auction, on_delete=models.CASCADE)


'''class Client(mongoengine.Document):
    id = models.BigAutoField(primary_key=True)
    user = mongoengine.IntField(unique=True)
    username = mongoengine.StringField(unique=True)
    password = mongoengine.StringField()
    balance = mongoengine.DecimalField(max_digits=10, decimal_places=2, default=0)
    watchlist = mongoengine.ListField()
    
    def __str__(self):
        return self.username'''
  