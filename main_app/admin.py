from django.contrib import admin
from .models import Trip, Item, City, My_Trip

# # Register your models here.

admin.site.register(Trip)
admin.site.register(Item)
admin.site.register(City)
admin.site.register(My_Trip)