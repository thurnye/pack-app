from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from datetime import datetime


# City Model
class City(models.Model):
    city_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    
    def __str__(self):
        return self.city_name

    def get_absolute_url(self):
        return reverse('searched_city', kwargs={'pk': self.id})

# Seasons
season = (
    ('WT', 'Winter'),
    ('SP', 'Spring'),
    ('SM', 'Summer'),
    ('FL', 'Fall'),
)

activity = (
    ("BP", "Backpacking"),
    ("SS", "Siteseeing"),
    ("LS", "Leisure"),
    ("BS", "Business"),
)

person = (
    ('Mn', 'Men'),
    ('Wm', 'Women'),
    ('By', 'Baby'),
)


class Item (models.Model):
    name = models.CharField(max_length=50)
    season = models.CharField(
        max_length=2,
        choices=season,
        # default=season[0][0],
    )
    activity = models.CharField(
        max_length=2,
        choices=activity,
        # default=activity[0][0],
    )
    person = models.CharField(
        max_length=2,
        choices=person,
        default=person[0][0],
    )
    vote = models.IntegerField(
        default=0
    )

    # 1:M model, establishing the foreign key
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return (f"{self.get_season_display()} on {self.name}")

    # sort by voting
    class Meta:
        ordering = ['-vote']

    # create the M:M
    user = models.ManyToManyField(User)

    # Link the user
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

# first

class My_Trip(models.Model):
    item = models.ManyToManyField(Item)
    

class Trip(models.Model):
     # 1:M model, establishing the foreign key
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default="Canada")
    # Link the user
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=datetime.now)
    #my_trip = models.ForeignKey(My_Trip, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50, null=True, default="")
    travelers = models.CharField(max_length=50, blank=True, null=True, default='')

# # second

# class Trip(models.Model):
#      # 1:M model, establishing the foreign key
#     city = models.CharField(max_length=50)
#     # Link the user
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField(' Date')

# class My_Trip(models.Model) :
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)