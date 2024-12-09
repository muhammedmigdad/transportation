from django.urls import path
from web import views

app_name = "web"

urlpatterns = [
   path("", views.index, name="index"),
   path("login/", views.login, name="login"),
   path("register/", views.register, name="register"),
   path("logout/", views.logout, name="logout"),
   path("validate_email/", views.validate_email, name="validate_email"),
   path("train", views.train, name="train"),
   path("bus", views.bus, name="bus"),
   
]