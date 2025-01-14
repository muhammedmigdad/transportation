from django.urls import path
from web import views

app_name = "web"

urlpatterns = [
   path("", views.index, name="index"),
   path("flight", views.flight, name="flight"),
   path("", views.index, name="index"),
   path("login/", views.login, name="login"),
   path("register/", views.register, name="register"),
   path("logout/", views.logout, name="logout"),
   path("validate_email/", views.validate_email, name="validate_email"),
   path("train/", views.train, name="train"),
   path("train-search/", views.train_search, name="train-search"),
   path("bus/", views.bus, name="bus"),
   path("bus-search/", views.bus_search, name="bus-search"),
   path("flight-books/<int:id>/", views.flight_books, name="flight-books"),
   path("offer/", views.offer, name="offer"),
   path("train-books/<int:id>/", views.train_books, name="train-books"),
   path("bus-books/<int:id>/", views.bus_books, name="bus-books"),
   path("bus-seat/", views.bus_seat, name="bus-seat"),
   path("train-seat/", views.train_seat, name="train-seat"),
   path("flight-class/<int:id>/", views.flight_class, name="flight-class"),
   path("flight-details/<int:id>/", views.flight_details, name="flight-details"),
   path('seat_selection/<int:id>/', views.seat_selection, name='seat_selection'),
   
]