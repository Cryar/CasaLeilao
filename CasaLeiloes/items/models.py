from django.db import models
from .mongo_settings import MONGODB_DATABASE

# Create your models here.

class ItemDocument(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = f"{MONGODB_DATABASE}.itemdocument"