from django.db import models
from PIL import Image
from django.db import models




class Product(models.Model):
    title = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    image_one = models.ImageField() 
    image_two = models.ImageField()
    image_three = models.ImageField()
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now = True)
   