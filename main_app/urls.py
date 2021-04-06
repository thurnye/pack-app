from django.contrib.auth import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path("trip/new/", views.new_trip, name="new_trip"),
    path("trip/<int:trip_id>/", views.trip, name="trip"),
    # path("trip/new/list", views.trip, name="new_trip"),
    path("profile/<int:user_id>/", views.profile, name="profile"),

    path("search/", views.search, name="search"),
    # path('search/', views.search_city, name='search_city'),
    path('search/new', views.searched_city, name='searched_city'),
    path('search/new/filters', views.searched_filters, name='searched_filters'),
    path('create', views.create, name="create"),

    path("test", views.test, name="test"),
    path("post/ajax/up", views.upvote_system, name="upvote_system"),
    path("post/ajax/down", views.downvote_system, name="downvote_system"),
    path("data/", views.generateData)
]
