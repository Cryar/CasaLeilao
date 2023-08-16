from django.contrib.auth.models import AbstractUser
from django.db import models
import mongoengine

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # Add other fields for user roles and profile

    def __str__(self):
        return self.username
    
from django.db import models
#from CasaLeiloes.settings import MONGOENGINE

# Create your models here.

class Produtos(models.Model):
    produto_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images/products')
    created_at = models.DateTimeField(auto_now_add=True)

    #class Meta:
     #   db_table = f"{MONGOENGINE}.itemdocument"
     
class Leiloes(models.Model):
    leilao_id = models.BigAutoField(primary_key=True, default=int)
    
class Watchlist(models.Model):
    watchlist_id = models.BigAutoField(primary_key=True, default=int)
    leiloes = models.ForeignKey(Leiloes, on_delete=models.CASCADE)
    
class Client(mongoengine.Document):
    id = models.BigAutoField(primary_key=True)
    user = mongoengine.IntField(unique=True)
    username = mongoengine.StringField(unique=True)
    password = mongoengine.StringField()
    balance = mongoengine.DecimalField(max_digits=10, decimal_places=2, default=0)
    watchlist = mongoengine.ListField()
    
    def __str__(self):
        return self.username