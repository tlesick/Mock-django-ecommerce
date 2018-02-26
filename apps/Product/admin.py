from django.contrib import admin
from apps.Product.models import *
from apps.Order.models import *

admin.site.register(Product)

admin.site.register(Order)