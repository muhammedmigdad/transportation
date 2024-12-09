from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import *
from users.models import User
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

@login_required(login_url='/login/')
def index(request):
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    flights = Flight.objects.all()
    airlineses = Airlines.objects.all()
    price = request.GET.get('price')
    airlines = request.GET.get('airlines')
    

    flight_duration = timedelta(days=1, hours=5, minutes=30)

    days = flight_duration.days
    total_seconds = flight_duration.total_seconds()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if airlines and airlines != 'all':
        airlines = airlines.filter(airlines__name=airlines)


    
    if price:
        if price == '3000-200000':
            flights = flights.filter(price__range=(3000, 200000))
        elif price == '3000-5000':
            flights = flights.filter(price__range=(3000, 5000))
        elif price == '10000-25000':
            flights = flights.filter(price__range=(10000,25000))
        elif price == '25000-40000':
            flights = flights.filter(price__range=(25000, 40000))
        elif price == '40000-60000':
            flights = flights.filter(price__range=(40000, 60000))
        elif price == '60000-80000':
            flights = flights.filter(price__range=(60000, 800000))
        elif price == '80000-100000':
            flights = flights.filter(price__range=(80000, 100000))
        elif price == '100000-200000':
            flights = flights.filter(price__range=(100000, 200000))
    
    
    sort_option = request.GET.get('sort', 'default')  

    if sort_option == 'latest':
        flights = flights.order_by('-created_on')
    elif sort_option == 'high-low':
        flights = flights.order_by('-price') 
    elif sort_option == 'low-high':
        flights = flights.order_by('price')  

    context = {
        'categories': categories,
        'sliders': sliders,
        'flights': flights,
        "minutes": minutes,
        "hours": hours,
        "days": days,
        "airlineses": airlineses,
    }

    return render(request, 'web/index.html', context=context)
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth_login  (request,user)
            return HttpResponseRedirect(reverse('web:index'))
        
        else:
            context = {
                'error': True,
                'message': 'Invalid  Email or Password'
            }
            return render(request, 'web/login.html', context=context)
            
        
    else:
        return render(request, 'web/login.html')
    
def  validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_valid' : User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            context = {
                'error': True,
                'message': 'Email Aleardy Exists'
            }
            return render(request, 'web/register.html', context=context)
        
        else:
            
        
        
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_customer=True
            )
            user.save()
            customer = Customer.objects.create(
                user=user
            )
            customer.save()
            return HttpResponseRedirect(reverse('web:login'))
    else:
        return render(request, 'web/register.html')
    
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('web:login'))
@login_required(login_url='/login/')
def train(request):
  
    return render(request, 'web/train.html')
@login_required(login_url='/login/')
def bus(request):
  
    return render(request, 'web/bus.html')