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

person = (
    ("A", "All"),
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
    name = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    season = models.CharField(max_length=10, choices=season, default=season[0][0])
    activity = models.CharField(max_length=10, choices=activity, default=activity[0][0])
    person = models.CharField(max_length=10, choices=person, default=person[0][0])
    gender = models.CharField(max_length=10, choices=gender, default=gender[0][0])
    vote = models.IntegerField(default=0)
    category = models.CharField(max_length=10, choices=category)

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
    city = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    season = models.CharField(
        max_length=10,
        choices=season,
    )
    activity = models.CharField(max_length=50, null=True, default="")
    travelers = models.CharField(max_length=50, blank=True, null=True, default='')


class Traveler(models.Model):
    name = models.CharField(max_length=25)


def getChoices(choices):
    return [x[1] for x in choices]
