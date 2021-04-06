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
    print(my_trips)
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


def search_city(request):
    return render(request, 'search_city.html')


def searched_city(request):
    return render(request, 'search_filters.html')


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
            season = "winter"
        elif(month == "04" or month == "05"):
            season = "spring"
        elif(month == "06" or month == "07" or month == "08" or month == "09"):
            season = "summer"
        elif(month == "10" or month == "11"):
            season = "fall"

        trip = Trip.objects.create(
            city=search[0],
            country=search[-1],
            date=date,
            season=season,
            # activity=# activity=request.POST.get('option1', '') == 'on',
            # travelers=request.POST.get('agegroup', False),
            user=request.user
        )
        trip.save()
        return redirect("/trip/%s/" % (trip.id))


# def trip_index(request, trip_id):
#     # if request.method == "GET":
#     return render(request, "trips/trip.html")


def trip(request, trip_id):
    if request.method == "GET":
        trip = Trip.objects.get(id=trip_id)

        items = Item.objects.filter(city=trip.city, country=trip.country, season=trip.season, activity=trip.activity)
        print(trip.user)
        return render(request, "trips/trip.html", {
            "categories": getChoices(category),
            "items": items


        })


def test(request):
    return render(request, "test.html")


def upvote_system(request):
    if request.is_ajax and request.method == "POST":
        print("UPVOTE: this is successfully an ajax & post method")
        # this is where the view func will update the database items counters
        # will also create a relation for the user, to check to see if they've previously voted
        return redirect('/')
    else:
        return JsonResponse({"error": ""}, status=400)


def downvote_system(request):
    if request.is_ajax and request.method == "POST":
        print("DOWNVOTE: this is successfully an ajax & post method")
        # this is where the view func will update the database items counters
        # will also create a relation for the user, to check to see if they've previously voted
        return redirect('/')
    else:
        return JsonResponse({"error": ""}, status=400)
