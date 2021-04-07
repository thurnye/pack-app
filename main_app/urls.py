from django.contrib.auth import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path("trip/new/", views.new_trip, name="new_trip"),
    path("trip/<int:trip_id>/", views.trip, name="trip"),
    path("profile/<int:user_id>/", views.profile, name="profile"),

    path("search/", views.search, name="search"),
    path('search/new/filters', views.searched_filters, name='searched_filters'),
    path('create', views.create, name="create"),

    path("post/ajax/up", views.upvote_system, name="upvote_system"),
    path("post/ajax/down", views.downvote_system, name="downvote_system"),





    path('findcity/', views.find_city, name="findcity"),
    path('findcity/results', views.results, name='results'),

    # Generate Data
    path("data/item/", views.itemData),
    path("data/item/<int:n>", views.itemData),
    path("data/user/", views.userData),
    path("data/user/<int:n>", views.userData),
    path("data/vote/", views.voteData),
    path("data/vote/<int:n>", views.voteData),
]
