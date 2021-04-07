from .generateData import generateItemData, generateUserData, generateVoteData
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from django.db.models import Sum, Q
from .models import User, Trip, Vote, Item, Activity, Traveler, CATEGORIES, ACTIVITIES, getChoices
import re

# Create your views here.


def home(request):
    trips = []
    my_trips = Trip.objects.filter(user_id=request.user.id)
    for my_trip in my_trips:
        trips.append({
            "trip": my_trip,
            "travelers": Traveler.objects.filter(trip_id=my_trip)
        })
    trips.reverse()

    return render(request, 'index.html', {
        "trips": trips[:3],
    })


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

@user_passes_test(lambda u: u.is_anonymous, '/')
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
            print("error")
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def new_trip(request):
    if request.method == "GET":
        activities = getChoices(ACTIVITIES)
        return render(request, "trips/trip_form.html", {
            "title": "Add New Trip",
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

            if sum_votes == None or sum_votes >= 0:
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
        return render(request, "trips/trip.html", {
            "title": "%s, %s" % (trip.city, trip.country),
            "categorized_items": categorized_items,
            "trip": trip_id,
            "activities": activities,
            "categories": categories,
        })


def itemData(request, n=100):
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


@ login_required
def upvote_system(request):
    if request.is_ajax and request.method == "POST":
        print("UPVOTE: this is successfully an ajax & post method")
        # this is where the view func will update the database items counters
        # will also create a relation for the user, to check to see if they've previously voted
        return redirect('/')
    else:
        return JsonResponse({"error": ""}, status=400)


@ login_required
def downvote_system(request):
    if request.is_ajax and request.method == "POST":
        print("DOWNVOTE: this is successfully an ajax & post method")
        # this is where the view func will update the database items counters
        # will also create a relation for the user, to check to see if they've previously voted
        return redirect('/')
    else:
        return JsonResponse({"error": ""}, status=400)


@ login_required
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
    items = Item.objects.filter(city__contains=search[0])[:num_items]
    categories = getChoices(CATEGORIES)
    sorted_items = {}
    for cat in categories:
        sorted_items[cat] = []
    for item in items:
        sorted_items[item.category].append(item)
    return render(request, 'search/results.html', {
        "categories": sorted_items,
    })


def add_item(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    new_item = Item.objects.create(
        name=request.POST['name'],
        city=trip.city,
        country=trip.country,
        season=request.POST['season'],
        activity=request.POST['activities'],
        category=request.POST['categories'],
        trip_id=trip_id
        # gender=
        # age=
        # public=
    )
    new_item.save()
    return redirect("/trip/%s/" % (trip_id))

def upcoming_trips(request):
    return render(request, "nav/upcomingtrips.html")