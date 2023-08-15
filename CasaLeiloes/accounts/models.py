from django.contrib.auth.models import AbstractUser
from django.db import models
import mongoengine

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # Add other fields for user roles and profile

    def __str__(self):
        return self.username
    
class Client(mongoengine.Document):
    id = models.BigAutoField(primary_key=True)
    user = mongoengine.IntField(unique=True)
    username = mongoengine.StringField(unique=True)
    password = mongoengine.StringField()
    balance = mongoengine.DecimalField(max_digits=10, decimal_places=2, default=0)
    watchlist = mongoengine.ListField(mongoengine.ReferenceField('items.Item'))

    def __str__(self):
        return self.username