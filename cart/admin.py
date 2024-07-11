from django.contrib import admin
from . import models
from .models import Cart, CartItem

admin.site.register(Cart )
admin.site.register(CartItem)
# Register your models here.
