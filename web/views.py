from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Category, Slider

def index(request):
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    context = {
        'categories': categories,
        "sliders": sliders
    }
    return render(request, 'web/index.html', context=context)