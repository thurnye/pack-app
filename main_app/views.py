from .generateData import generateItemData, generateUserData, generateVoteData
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from django.db.models import Sum, Q
from dotenv import load_dotenv
load_dotenv()
import os
import requests
from .models import User, Trip, Vote, Item, Activity, Traveler, CATEGORIES, ACTIVITIES, SEASONS, AGES, GENDERS, getChoices
import re, json
import requests

from datetime import date
import ast

# config = dotenv_values(".env")
# Create your views here.


def home(request):
    trips = []
    my_trips = Trip.objects.filter(user_id=request.user.id)
    past_trips = False
    today = date.today()
    for my_trip in my_trips:
        if my_trip.date < today:
            past_trips = True
        trips.append({
            "trip": my_trip,
            "travelers": Traveler.objects.filter(trip_id=my_trip)
        })
    trips.reverse()

    return render(request, 'index.html', {
        "trips": trips[:3],
        "past_trips": past_trips,
    })

@user_passes_test(lambda u: u.is_anonymous, '/')
def signup(request):
    error_message = ''
    if request.method == 'POST':
        print(request.POST)
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
            print("Invalid sign up - try again")
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def search(request):
    if request.method == "POST":
        print(request.POST)
        return render(request, "results.html", {
            "destination": request.POST["destination"],
            "activity": request.POST["activity"],
            "date": request.POST["date"]
        })


def searched_filters(request):
    return render(request, 'results.html')


def create(request):
    return redirect('search/new/filters')

@login_required
def new_trip(request):
    if request.method == "GET":
        activities = getChoices(ACTIVITIES)
        return render(request, "trips/trip_form.html", {
            "title": "Add New Trip",
            "previous_url": {
                "url": "/",
                "text": "All Trips"
            },
            "activities": activities,
        })
    elif request.method == "POST":
        body = request.POST

        search = re.split(', | - ', body['search'])
        date = body["date"]
        month = date.split("-")[1]
        day = date.split("-")[2]
        if (month == "12" or month == "01" or month == "02" or month == "03"):
            season = "Winter"
        elif(month == "04" or month == "05"):
            season = "Spring"
        elif(month == "06" or month == "07" or month == "08" or month == "09"):
            season = "Summer"
        elif(month == "10" or month == "11"):
            season = "Fall"
        number_items = int(body["number_items"])

        trip = Trip.objects.create(
            user=request.user,
            city=search[0].title(),
            country=search[-1].title(),
            date=date,
            season=season.title(),
            number_items=number_items
        )
        trip.save()

        activities = body.getlist("activities")
        for activity in activities:
            newActivity = Activity.objects.create(
                trip=trip,
                activity=activity,
            )
            newActivity.save()

        traveler_names = body.getlist("name")
        genders = body.getlist("gender")
        ages = body.getlist("age")

        for i in range(len(traveler_names)):
            traveler = Traveler.objects.create(
                trip=trip,
                name=traveler_names[i],
                gender=genders[i],
                age=ages[i]
            )
            traveler.save()

        return redirect("/trip/%s/" % (trip.id))


@login_required
def trip(request, trip_id):
    if request.method == "GET":
        trip = Trip.objects.get(id=trip_id)
        if trip.user != request.user:
            return redirect("/")

        activities = Activity.objects.filter(trip_id=trip.id)
        filtered_items = []
        for i in range(len(activities)):
            filtered_items_temp = Item.objects.filter(city=trip.city, country=trip.country, season=trip.season, activity=activities[i].activity, trip_id=None, public=True)
            filtered_items.extend(filtered_items_temp)
        filtered_items = list(set(filtered_items))

        filtered_items.extend(Item.objects.filter(trip_id=trip.id))

        items = []
        personal_items = []
        for item in filtered_items:
            sum_votes = Vote.objects.filter(item_id=item.id).aggregate(Sum("vote"))["vote__sum"]
            user_item = Vote.objects.filter(item_id=item.id, user_id=request.user.id)
            if len(user_item) == 1:
                vote = user_item[0]
            else:
                vote = Vote.objects.create(
                    item_id=item.id,
                    user_id=request.user.id,
                    vote=0,
                    checked=False
                )

            if sum_votes == None:
                sum_votes = 0
            
            if sum_votes >= 0:
                if item.trip_id == trip.id:
                    personal_items.append({
                        "item": item,
                        "sum_votes": sum_votes,
                        "vote": vote,
                        "personal": True
                    })
                else:
                    items.append({
                        "item": item,
                        "sum_votes": sum_votes,
                        "vote": vote,
                        "personal": False
                    })
        sorted_items = sorted(items, key=lambda k: k["sum_votes"], reverse=True)[:trip.number_items]
        sorted_items.extend(personal_items)

        categories = getChoices(CATEGORIES)
        categorized_items = {}
        for category in categories:
            categorized_items[category] = []

        for i in range(len(sorted_items)):
            old_item = sorted_items[i]
            categorized_items[old_item["item"].category].append(old_item)
        activities = getChoices(ACTIVITIES)
        # weather api call below this line
        city = "%s,%s" % (trip.city,trip.country)
        key = os.environ.get("WEATHER_KEY")
        api = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={key}&include=obs%2Cfcst%2Calerts%2Ccurrent%2Chistfcst"
        data = requests.get(api).json()
        weather_forecast = data['days']
        current_temp_high = f"{int(data['days'][0]['tempmax'])}\u00B0C"
        current_temp_low = f"{int(data['days'][0]['tempmin'])}\u00B0C"
        icon = data['days'][0]['icon']
        current_condition = data['days'][0]['conditions']

        
        return render(request, "trips/trip.html", {
            "title": "%s, %s" % (trip.city, trip.country),
            "categorized_items": categorized_items,
            "activities": activities,
            "categories": categories,
            "seasons" : getChoices(SEASONS),
            "ages" : getChoices(AGES),
            "genders" : getChoices(GENDERS),
            "trip": trip,
            "forecast" : weather_forecast,
            "today_temp_high" : current_temp_high,
            "today_temp_low" : current_temp_low,
            "condition" : current_condition,
            'weather_icon' : icon,
        })

@login_required
def edit_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    travelers = Traveler.objects.filter(trip_id=trip.id)
    return render(request, "trips/trip_form.html", {
        "trip": trip,
        "travellers": travelers,
        "activities" : getChoices(ACTIVITIES),
        "genders" : getChoices(GENDERS),
    })

@login_required
def delete_trip(request, trip_id):
    pass

@login_required
def add_item(request, trip_id):
    body = request.POST
    print(body)
    trip = Trip.objects.get(id=trip_id)
    new_item = Item.objects.create(
        name=body['name'],
        city=trip.city,
        country=trip.country,
        season=body['season'],
        activity=body['activities'],
        gender=body["gender"],
        age=body["age"],
        category=body['category'],
        trip_id=trip_id,
        # public=public
    )
    new_item.save()
    return redirect("/trip/%s/" % (trip_id))

def item(request, trip_id, item_id):
    pass

def edit_item(request, trip_id, item_id):
    pass

def delete_item(request, trip_id, item_id):
    pass


@login_required
def upcoming_trips(request):
    trips = []
    my_trips = Trip.objects.filter(user_id=request.user.id)
    today = date.today()
    for my_trip in my_trips:
        if my_trip.date >= today:
            trips.append({
                "trip": my_trip,
                "travelers": Traveler.objects.filter(trip_id=my_trip)
            })
    trips.reverse()
    return render(request, "trips/upcoming_trips.html", {
        "previous_url": {
            "url": "/",
            "text": "All Trips"
        },
        "trips": trips,
    })


@login_required
def past_trips(request):
    trips = []
    my_trips = Trip.objects.filter(user_id=request.user.id)
    today = date.today()
    for my_trip in my_trips:
        if my_trip.date < today:
            trips.append({
                "trip": my_trip,
                "travelers": Traveler.objects.filter(trip_id=my_trip)
            })
    trips.reverse()
    return render(request, "trips/past_trips.html", {
        "previous_url": {
            "url": "/",
            "text": "All Trips"
        },
        "trips": trips,
    })

@login_required
def vote(request):
    if request.method == "POST":
        body = ast.literal_eval(request.body.decode())
        trip = Trip.objects.get(id=int(body["trip_id"]))
        changeValue = int(body["change_value"])
        user = trip.user
        item = Item.objects.get(id=int(body["item_id"]))
        vote = Vote.objects.get(user_id=user.id, item_id=item.id)
        vote.vote += changeValue
        vote.save()
        
        return JsonResponse({},status=200)

@login_required
def profile(request, user_id):
    my_trips = Trip.objects.filter(user_id=user_id)
    my_items = []
    for trip in my_trips:
        found_item = Item.objects.filter(trip_id=trip.id).first()
        if found_item:
            my_items.append(found_item)
    return render(request, 'registration/profile.html', {
        "mytrips": my_trips,
        "my_items": my_items,
    })


def find_city(request):
    activities = getChoices(ACTIVITIES)
    return render(request, 'search/search.html', {
        "activities": activities,
    })


def results(request):
    search = re.split(', | - ', request.POST['search'])
    num_items = int(request.POST['number_items'])
    date = request.POST["date"]
    month = date.split("-")[1]
    day = date.split("-")[2]
    if (month == "12" or month == "01" or month == "02" or month == "03"):
        season = "Winter"
    elif(month == "04" or month == "05"):
        season = "Spring"
    elif(month == "06" or month == "07" or month == "08" or month == "09"):
        season = "Summer"
    elif(month == "10" or month == "11"):
        season = "Fall"
    items = Item.objects.filter(city__contains=search[0], season=season)[:num_items]
    categories = getChoices(CATEGORIES)
    sorted_items = {}
    for cat in categories:
        sorted_items[cat] = []
    for item in items:
        sorted_items[item.category].append(item)
    key = os.environ.get("KEY")
    city = search[0]
    api = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={key}&include=obs%2Cfcst%2Calerts%2Ccurrent%2Chistfcst"
    data = requests.get(api).json()
    weather_forecast = data['days']
    current_temp_high = f"{int(data['days'][0]['tempmax'])}\u00B0C"
    current_temp_low = f"{int(data['days'][0]['tempmin'])}\u00B0C"
    icon = data['days'][0]['icon']
    current_condition = data['days'][0]['conditions']
    return render(request, 'search/results.html', {
        "categories": sorted_items,
        "forecast" : weather_forecast,
        "today_temp_high" : current_temp_high,
        "today_temp_low" : current_temp_low,
        "condition" : current_condition,
        'weather_icon' : icon,
        "city": city,
    })
    

def itemData(request, n=50000):
    data = generateItemData(n)
    return render(request, "data.html", {
        "data": data
    })


def userData(request, n=10):
    data = generateUserData(n)
    return render(request, "data.html", {
        "data": data
    })


def voteData(request, n=1000):
    data = generateVoteData(n)
    return render(request, "data.html", {
        "data": data
    })

def index_search(request):
    search = re.split(', | - ', request.POST['search'])
    num_items = 15
    items = Item.objects.filter(city__contains=search[0])[:num_items]
    categories = getChoices(CATEGORIES)
    sorted_items = {}
    for cat in categories:
        sorted_items[cat] = []
    for item in items:
        sorted_items[item.category].append(item)
        city = search[0]
    key = os.environ.get("KEY")
    api = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={key}&include=obs%2Cfcst%2Calerts%2Ccurrent%2Chistfcst"
    data = requests.get(api).json()
    weather_forecast = data['days']
    current_temp_high = f"{int(data['days'][0]['tempmax'])}\u00B0C"
    current_temp_low = f"{int(data['days'][0]['tempmin'])}\u00B0C"
    icon = data['days'][0]['icon']
    current_condition = data['days'][0]['conditions']
    return render(request, 'search/index_results.html', {
        "categories": sorted_items,
        "forecast" : weather_forecast,
        "today_temp_high" : current_temp_high,
        "today_temp_low" : current_temp_low,
        "condition" : current_condition,
        'weather_icon' : icon,
        "city": search[0],
    })
