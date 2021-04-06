from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from datetime import datetime

season = (
    ('AL', 'All'),
    ('WT', 'Winter'),
    ('SP', 'Spring'),
    ('SM', 'Summer'),
    ('FL', 'Fall'),
)

activity = (
    ("AL", "All"),
    ("BP", "Backpacking"),
    ("SS", "Sightseeing"),
    ("LS", "Leisure"),
    ("BS", "Business"),
    ("OT", "Other")
)

age = (
    ("A", "All Ages"),
    ("I", "Infant"),
    ("C", "Child"),
    ("T", "Teen"),
    ("A", "Adult"),
    ("S", "Senior")
)

gender = (
    ("A", "All"),
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other")
)

category = (
    ("CL", "Clothing"),
    ("EL", "Electronics"),
    ("EQ", "Equipment"),
    ("PS", "Personal"),
    ("MD", "Medication"),
    ("OT", "Other"),
)


class Item (models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    season = models.CharField(max_length=25, choices=season, default=season[0][1])
    activity = models.CharField(max_length=25, choices=activity, default=activity[0][1])
    age = models.CharField(max_length=25, choices=age, default=age[0][1])
    gender = models.CharField(max_length=25, choices=gender, default=gender[0][1])
    vote = models.IntegerField(default=0)
    category = models.CharField(max_length=25, choices=category)
    trip_id = models.IntegerField(null=True)

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


class Trip(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    season = models.CharField(max_length=25, choices=season, default=season[0][1])
    activity = models.CharField(max_length=50, default=activity[0][1])
    travelers = models.CharField(max_length=50, default='')
    # num_items = models.IntegerField(default=15)


class Traveler(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=25)
    gender = models.CharField(max_length=25, choices=gender, default=gender[0][1])
    age = models.CharField(max_length=25, choices=age, default=age[0][1])
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True)


def getChoices(choices):
    return [x[1] for x in choices]
