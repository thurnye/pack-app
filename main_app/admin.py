from django.contrib import admin
from .models import Trip, Item, Traveler

# # Register your models here.

admin.site.register(Trip)
admin.site.register(Item)
admin.site.register(Traveler)
