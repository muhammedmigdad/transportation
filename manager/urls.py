from django.urls import path
from manager import views

app_name = "manager"

urlpatterns = [
    
   path("", views.index, name="index"),
   path("login/", views.login, name="login"),
   path("logout/", views.logout, name="logout"),
   path("slider/", views.slider, name="slider"),
   path("slider_add", views.slider_add, name="slider_add"),
   path("slider_edit/<int:id>/", views.slider_edit, name="slider_edit"),
   path("slider_delete/<int:id>/", views.slider_delete, name="slider_delete"), 
   path("users/", views.users, name="users"),
   path("users_delete/<int:id>/", views.users_delete, name="users_delete"),
   path("users_edit/<int:id>/", views.users_edit, name="users_edit"),
   path("users_add/", views.users_add, name="users_add"),
   path("offers/", views.offers, name="offers"),
   path("offers_add", views.offers_add, name="offers_add"),
   path("offers_edit/<int:id>/", views.offers_edit, name="offers_edit"),
   path("offers_delete/<int:id>/", views.offers_delete, name="offers_delete"),
]