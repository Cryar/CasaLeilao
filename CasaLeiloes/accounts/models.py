from django.contrib.auth.models import AbstractUser
from django.db import models
import mongoengine
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
# Create your models here.

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # Add other fields for user roles and profile

    def __str__(self):
        return self.username
#from CasaLeiloes.settings import models

# Create your models here.
class Lotes(models.Model):
    lot_id = models.AutoField(primary_key=True)
    lot_name = models.CharField(max_length=50)
    description = models.TextField()

class Produtos(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lotes, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ProdutosImage(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.image.url

class Leiloes(models.Model):
    auction_id = models.BigAutoField(primary_key=True, default=int)
    number_of_bids = models.IntegerField()
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    minimum_increment = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)

class Watchlist(models.Model):
    watchlist_id = models.BigAutoField(primary_key=True, default=int)
    auctions = models.ForeignKey(Leiloes, on_delete=models.CASCADE)
    
class watchlist_user(models.Model):
    watchlist_user_id = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, models.CASCADE)
    

class Licitacoes(models.Model):
    bid_id = models.IntegerField(primary_key=True, serialize=True, unique=True)
    user = models.IntegerField()
    bid_time = models.DateTimeField()
    minimum_value = models.DecimalField(max_digits=6, decimal_places=2)
    final_value = models.DecimalField(max_digits=6, decimal_places=2)

class Centro_custo(models.Model):
    cost_center_id = models.AutoField(primary_key=True)
    cost_center_date = models.DateField()
    bid = models.ForeignKey(Licitacoes,on_delete=models.CASCADE)

class Client(mongoengine.Document):
    id = models.BigAutoField(primary_key=True)
    user = mongoengine.IntField(unique=True)
    username = mongoengine.StringField(unique=True)
    password = mongoengine.StringField()
    balance = mongoengine.DecimalField(max_digits=10, decimal_places=2, default=0)
    watchlist = mongoengine.ListField()
    
    def __str__(self):
        return self.username
    
class BiddingHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    leilao = models.ForeignKey(Leiloes, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)