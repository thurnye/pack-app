import random
from .models import Item, season, activity, age, gender, category, getChoices
from .static.data.places import cities
from .static.data.names import item_names

season_choices = getChoices(season)
activity_choices = getChoices(activity)
age_choices = getChoices(age)
gender_choices = getChoices(gender)
category_choices = getChoices(category)


def getData(n):
    data = []
    for i in range(n):
        random_city = cities[random.randint(0, len(cities)-1)]

        Item.objects.create(
            name=item_names[random.randint(0, len(item_names)-1)].title(),
            city=random_city["City"].title(),
            country=random_city["Country"].title(),
            season=season_choices[random.randint(0, len(season_choices)-1)].title(),
            activity=activity_choices[random.randint(0, len(activity_choices)-1)].title(),
            age=age_choices[random.randint(0, len(age_choices)-1)].title(),
            gender=gender_choices[random.randint(0, len(gender_choices)-1)].title(),
            vote=random.randint(-999, 4999),
            category=category_choices[random.randint(0, len(category_choices)-1)].title(),
            trip_id=None
        )
        name = item_names[random.randint(0, len(item_names)-1)]
        city = random_city["City"]
        country = random_city["Country"]
        # s = season_choices[random.randint(0, len(season_choices)-1)]
        # a = activity_choices[random.randint(0, len(activity_choices)-1)]
        # p = age_choices[random.randint(0, len(age_choices)-1)]
        # g = gender_choices[random.randint(0, len(gender_choices)-1)]
        # c = category_choices[random.randint(0, len(category_choices)-1)]
        data.append({
            i, name, city, country
        })
    return data
