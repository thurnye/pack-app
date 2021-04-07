from .generateData import getData
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .models import Item, Trip, User, category, activity, getChoices

# Create your views here.

def home(request):
    my_trips = Trip.objects.filter(user_id=request.user.id)
    activities = [x[1] for x in activity]
    return render(request, 'index.html', {
        "mytrips": my_trips,
        "activities": activities,
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


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def new_trip(request):
    if request.method == "GET":
        return render(request, "trips/trip_form.html", {
            
        })
    elif request.method == "POST":
        print(request.POST)
        search = request.POST['search'].split(", ")
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

        trip = Trip.objects.create(
            city=search[0].title(),
            country=search[-1].title(),
            date=date,
            season=season.title(),
            # activity=# activity=request.POST.get('option1', '') == 'on',
            # travelers=request.POST.get('agegroup', False),
            user=request.user
        )
        trip.save()
        return redirect("/trip/%s/" % (trip.id))


# def trip_index(request, trip_id):
#     # if request.method == "GET":
#     return render(request, "trips/trip.html")

@login_required
def trip(request, trip_id):
    if request.method == "GET":
        trip = Trip.objects.get(id=trip_id)
        num_items = 15
        items = Item.objects.filter(city=trip.city, country=trip.country, season=trip.season, activity=trip.activity)[:num_items]
        categories = getChoices(category)
        sorted_items = {}
        for cat in categories:
            sorted_items[cat] = []
        for item in items:
            if item.vote > 0:
                sorted_items[item.category].append(item)

        # print(trip.city, trip.country, trip.season, trip.activity)
        # personal_items = Item.objects.filter(city=trip.city, country=trip.country, season=trip.season, activity=trip.activity, trip_id=trip.id)
        # for cat in sorted_items:
        #     for i in cat:
        #         print(i)

        return render(request, "trips/trip.html", {
            "title": "%s, %s" % (trip.city, trip.country),
            "categories": sorted_items,
            # "items": sorted_items,
            # "personal_items": personal_items
        })


def generateData(request):
    data = getData(10000)
    return render(request, "data.html", {
        "data": data
    })

@login_required
def upvote_system(request):
    if request.is_ajax and request.method == "POST":
        print("UPVOTE: this is successfully an ajax & post method")
        # this is where the view func will update the database items counters
        # will also create a relation for the user, to check to see if they've previously voted
        return redirect('/')
    else:
        return JsonResponse({"error": ""}, status=400)

@login_required
def downvote_system(request):
    if request.is_ajax and request.method == "POST":
        print("DOWNVOTE: this is successfully an ajax & post method")
        # this is where the view func will update the database items counters
        # will also create a relation for the user, to check to see if they've previously voted
        return redirect('/')
    else:
        return JsonResponse({"error": ""}, status=400)

@login_required
def profile(request, user_id):
    my_trips = Trip.objects.filter(user_id=user_id)
    my_items = Item.objects.filter(user=user_id)
    return render (request, 'registration/profile.html', {
        "mytrips": my_trips,
        "myitems": my_items,
    })