from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from users.models import User
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import BusSeatStatusForm
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/login/')
def seat_selection(request, id):
    bus = get_object_or_404(Bus, id=id)
    seats = BusSeatStatus.objects.filter(buses=bus)
    if request.method == "POST":
        selected_seats = request.POST.getlist('selected_seats')
        for id in selected_seats:
            seat = BusSeatStatus.objects.get(id=id)
            if seat.status == "available":
                seat.status = "booked"
                seat.save()
        return render(request, 'web/bus-books.html', {'bus': bus, 'selected_seats': selected_seats})

    context = {
        'bus': bus,
        'seats': seats,
    }
    return render(request, 'web/bus-seat.html', context=context)




@login_required(login_url='/login/')
def index(request):
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    flights = Flight.objects.all()
    airlineses = Airlines.objects.all()
    price = request.GET.get('price')
    selected_airline = request.GET.get('category', 'all')
    selected_stop = request.GET.get('Stop', '')
    selected_airline = request.GET.get('airline', None)
    price_min = request.GET.get('price_min', None)
    price_max = request.GET.get('price_max', None)
    
    if selected_airline and selected_airline != 'all':
        flights = flights.filter(airline__name=selected_airline)

    if price_min and price_max:
        flights = flights.filter(price__range=(price_min, price_max))

    if request.method == "POST":
        adults = int(request.POST.get('adults', 0))
        children = int(request.POST.get('children', 0))
        infants = int(request.POST.get('infants', 0))
        travel_class = request.POST.get('class', 'economy')
        
        request.session['travel_details'] = {
            'adults': adults,
            'children': children,
            'infants': infants,
            'class': travel_class,
        }
        
        return JsonResponse({'message': 'Travel details updated successfully!'})

    travel_details = request.session.get('travel_details', {
        'adults': 1,
        'children': 0,
        'infants': 0,
        'class': 'economy',
    })
    
    if selected_stop:
        if selected_stop == 'Non Stop':
            flights = flights.filter(stops='Non-stop')  
        elif selected_stop == 'one Stop':
            flights = flights.filter(stops='1 stop')
            

    if selected_airline and selected_airline != 'all':
        flights = flights.filter(airline__name=selected_airline)
        
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
    elif sort_option == 'Faster':
        flights = flights.order_by('duration')  
        
    context = {
        'categories': categories,
        'sliders': sliders,
        'flights': flights,
        "airlineses": airlineses,
        "travel_details":travel_details
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
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    trains = Train.objects.all()
    trainses = Trains.objects.all()
    price = request.GET.get('price')
    selected_trainses = request.GET.get('category', 'all')
    selected_stop = request.GET.get('Stop', '')

    if selected_stop:
        if selected_stop == 'Non Stop':
            trains = trains.filter(stops='Non-stop')  
        elif selected_stop == 'one Stop':
            trains = trains.filter(stops='1 stop')
        elif selected_stop == 'Limited Stop':
            trains = trains.filter(stops='Limited Stop')
            

    if selected_trainses and selected_trainses != 'all':
        trains = trains.filter(trains__name=selected_trainses)
        
    if price:
        if price == '3000-200000':
            trains = trains.filter(price__range=(3000, 200000))
        elif price == '3000-5000':
            trains = trains.filter(price__range=(3000, 5000))
        elif price == '10000-25000':
            trains = trains.filter(price__range=(10000, 25000))
        elif price == '25000-40000':
            trains = trains.filter(price__range=(25000, 40000))
        elif price == '40000-60000':
            trains = trains.filter(price__range=(40000, 60000))
        elif price == '60000-80000':
            trains = trains.filter(price__range=(60000, 800000))
        elif price == '80000-100000':
            trains = trains.filter(price__range=(80000, 100000))
        elif price == '100000-200000':
            trains = trains.filter(price__range=(100000, 200000))
    
    
    sort_option = request.GET.get('sort', 'default')  

    if sort_option == 'latest':
        trains = trains.order_by('-created_on')
    elif sort_option == 'high-low':
        trains = trains.order_by('-price') 
    elif sort_option == 'low-high':
        trains = trains.order_by('price')  
    elif sort_option == 'Faster':
        trains = trains.order_by('duration')  
    
    context = {
        'categories': categories,
        'sliders': sliders,
        "trains": trains,
        "trainses": trainses,
    }
    return render(request, 'web/train.html', context=context)
@login_required(login_url='/login/')
def bus(request):
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    bus = Bus.objects.all()
    buses = Buses.objects.all()
    price = request.GET.get('price')
    selected_bus = request.GET.get('category', 'all')
    selected_stop = request.GET.get('Stop', '')

    if selected_stop:
        if selected_stop == 'Non Stop':
            bus = bus.filter(stops='Non-stop')  
        elif selected_stop == 'one Stop':
            bus = bus.filter(stops='1 stop')
        elif selected_stop == 'one Stop':
            bus = bus.filter(stops='Limited Stop')
            
            

    if selected_bus and selected_bus != 'all':
        bus = bus.filter(Buses__name=selected_bus)
        
    if price:
        if price == '500-20000':
            bus = bus.filter(price__range=(500, 20000))
        elif price == '500-1000':
            bus = bus.filter(price__range=(500, 1000))
        elif price == '1000-2000':
            bus = bus.filter(price__range=(1000,2000))
        elif price == '2000-4000':
            bus = bus.filter(price__range=(2000, 4000))
        elif price == '4000-6000':
            bus = bus.filter(price__range=(4000, 6000))
        elif price == '6000-8000':
            bus = bus.filter(price__range=(6000, 8000))
        elif price == '8000-10000':
            bus = bus.filter(price__range=(8000, 10000))
        elif price == '100000-200000':
            bus = bus.filter(price__range=(10000, 20000))
    
    
    sort_option = request.GET.get('sort', 'default')  

    if sort_option == 'latest':
        bus = bus.order_by('-created_on')
    elif sort_option == 'high-low':
        bus = bus.order_by('-price') 
    elif sort_option == 'low-high':
        bus = bus.order_by('price')  
    elif sort_option == 'Faster':
        bus = bus.order_by('duration')  
    
    context = {
        'categories': categories,
        'sliders': sliders,
        "bus": bus,
        "buses": buses
    }
    return render(request, 'web/bus.html', context=context)

def flight_books(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    fligths = Flight.objects.get(id=id)
    if CartBill.objects.filter(customer=customer).exists():
        cartbill = CartBill.objects.get(customer=customer)
        cartbill.item_total = float(fligths.price)  
        cartbill.tax_charge = 100.00 
        cartbill.totel_amount = fligths.price + 100  
        cartbill.offer_amount = 0.00 
        cartbill.save()
    else:
        cartbill = CartBill.objects.create(
            customer=customer,
            item_total=float(fligths.price), 
            tax_charge=100.00, 
            totel_amount=fligths.price + 100,  
            offer_amount=0.00  
        )
        cartbill.save()

        
        
    if FlightBill.objects.filter(fligths=fligths).exists():
        flightbill = FlightBill.objects.get(fligths=fligths)
        flightbill.airline_name = fligths.airline.name 
        flightbill.flight_code = fligths.flight_numbers
        flightbill.departure_time = fligths.departure_time
        flightbill.arrival_time = fligths.arrival_time
        flightbill.duration = fligths.duration
        flightbill.departure_airport = fligths.departure_code
        flightbill.arrival_airport = fligths.arrival_code
        flightbill.fligths.price
        flightbill.save()
    else:
        flightbill = FlightBill.objects.create(
            fligths=fligths,
            airline_name=fligths.airline.name, 
            flight_code=fligths.flight_numbers,
            departure_time=fligths.departure_time,
            arrival_time=fligths.arrival_time,
            duration=fligths.duration,
            departure_airport=fligths.departure_code,
            arrival_airport=fligths.arrival_code,
            baggage_allowance='20 Kg Total in 2 Pieces',
            cabin_baggage='7 Kg',
            check_in_baggage='20 Kg',
            terminal='IN',
            status='On-time'
        )



    cart_items = FlightBill.objects.get(fligths=fligths)
    
    
    error_message = None
    

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            offer = Offer.objects.get(code=code) 
            
            if offer.is_percentage:
                discount = round((offer.discount / 100) * cartbill.item_total, 2)
            else:
                discount = offer.discount

            discount = min(discount, cartbill.item_total)

            cartbill.offer_amount = discount
            cartbill.total_amount = cartbill.item_total + cartbill.tax_charge - discount
            cartbill.save()
            success_message = 'Coupon code applied successfully!'
        except Offer.DoesNotExist:
            error_message = 'Invalid coupon code. Please try again.'


    context = {
        "cart_items": cart_items,
        "fligths": fligths,
        "flightbill": flightbill,
        "cartbill": cartbill,
        "error_message": error_message,
        "success_message": success_message if 'success_message' in locals() else None,

    }

    return render(request, 'web/flight-books.html', context=context)


def offer(request):
    sliders = Slider.objects.all()
    
    
    context = {
        "sliders": sliders,
    }
    
    return render(request, 'web/offer.html', context=context)

def train_books(request, id):  
    user = request.user
    customer = Customer.objects.get(user=user)
    trains = Train.objects.get(id=id)
    if CartBill.objects.filter(customer=customer).exists():
        cartbill = CartBill.objects.get(customer=customer)
        cartbill.item_total = float(trains.price)  
        cartbill.tax_charge = 100.00 
        cartbill.totel_amount = trains.price + 100  
        cartbill.offer_amount = 0.00 
        cartbill.save()
    else:
        cartbill = CartBill.objects.create(
            customer=customer,
            item_total=float(trains.price), 
            tax_charge=100.00, 
            totel_amount=trains.price + 100,  
            offer_amount=0.00  
        )
        cartbill.save()

        
        
    if TrainDetail.objects.filter(trains=trains).exists():
        traindetail = TrainDetail.objects.get(trains=trains)
        traindetail.train_name = trains.trains.name 
        traindetail.train_code = trains.train_numbers
        traindetail.departure_time = trains.departure_time
        traindetail.arrival_time = trains.arrival_time
        traindetail.duration = trains.duration
        traindetail.departure_stop = trains.departure_code
        traindetail.arrival_stop = trains.arrival_code
        traindetail.trains.price
        traindetail.save()
    else:
        traindetail = TrainDetail.objects.create(
            trains=trains,
            train_name=trains.trains.name, 
            train_code=trains.train_numbers,
            departure_time=trains.departure_time,
            arrival_time=trains.arrival_time,
            duration=trains.duration,
            departure_stop=trains.departure_code,
            arrival_stop=trains.arrival_code,
            baggage_allowance='10 Kg ',
            cabin_baggage='3 Kg',
            check_in_baggage='10 Kg',
            terminal='IN',
            status='On-time'
        )



    cart_items = TrainDetail.objects.get(trains=trains)
    
    error_message = None
    

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            offer = Offer.objects.get(code=code) 
            
            if offer.is_percentage:
                discount = round((offer.discount / 100) * cartbill.item_total, 2)
            else:
                discount = offer.discount

            discount = min(discount, cartbill.item_total)

            cartbill.offer_amount = discount
            cartbill.total_amount = cartbill.item_total + cartbill.tax_charge - discount
            cartbill.save()
            success_message = 'Coupon code applied successfully!'
        except Offer.DoesNotExist:
            error_message = 'Invalid coupon code. Please try again.'


    context = {
        "cart_items": cart_items,
        "trains": trains,
        "traindetail": traindetail,
        "cartbill": cartbill,
        "error_message": error_message,
        "success_message": success_message if 'success_message' in locals() else None,
    }


    return render(request, 'web/train-books.html',context=context)

def bus_books(request, id):  
    user = request.user
    customer = Customer.objects.get(user=user)
    buses = Bus.objects.get(id=id)
    if CartBill.objects.filter(customer=customer).exists():
        cartbill = CartBill.objects.get(customer=customer)
        cartbill.item_total = float(buses.price)  
        cartbill.tax_charge = 100.00 
        cartbill.totel_amount = buses.price + 100  
        cartbill.offer_amount = 0.00 
        cartbill.save()
    else:
        cartbill = CartBill.objects.create(
            customer=customer,
            item_total=float(buses.price), 
            tax_charge=100.00, 
            totel_amount=buses.price + 100,  
            offer_amount=0.00  
        )
        cartbill.save()

        
        
    if BusDetail.objects.filter(buses=buses).exists():
        busdetail = BusDetail.objects.get(buses=buses)
        busdetail.bus_name = buses.buses.name 
        busdetail.bus_code = buses.bus_numbers
        busdetail.departure_time = buses.departure_time
        busdetail.arrival_time = buses.arrival_time
        busdetail.duration = buses.duration
        busdetail.departure_stop = buses.departure_code
        busdetail.arrival_stop = buses.arrival_code
        busdetail.buses.price
        busdetail.save()
    else:
        busdetail = BusDetail.objects.create(
            buses=buses,
            bus_name=buses.buses.name, 
            bus_code=buses.bus_numbers,
            departure_time=buses.departure_time,
            arrival_time=buses.arrival_time,
            duration=buses.duration,
            departure_stop=buses.departure_code,
            arrival_stop=buses.arrival_code,
            baggage_allowance='5 Kg ',
            cabin_baggage='2 Kg',
            check_in_baggage='5 Kg',
            terminal='IN',
            status='On-time'
        )



    cart_items = BusDetail.objects.get(buses=buses)
    
    error_message = None
    

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            offer = Offer.objects.get(code=code) 
            
            if offer.is_percentage:
                discount = round((offer.discount / 100) * cartbill.item_total, 2)
            else:
                discount = offer.discount

            discount = min(discount, cartbill.item_total)

            cartbill.offer_amount = discount
            cartbill.total_amount = cartbill.item_total + cartbill.tax_charge - discount
            cartbill.save()
            success_message = 'Coupon code applied successfully!'
        except Offer.DoesNotExist:
            error_message = 'Invalid coupon code. Please try again.'


    context = {
        "cart_items": cart_items,
        "buses": buses,
        "busdetail": busdetail,
        "cartbill": cartbill,
        "error_message": error_message,
        "success_message": success_message if 'success_message' in locals() else None,
    }


    return render(request, 'web/bus-books.html',context=context)


def bus_seat(request):
    
    bus = Bus.objects.all()
    
    
    context = {
        "bus": bus,
    }
    
    return render(request, 'web/bus-seat.html', context=context)
def train_seat(request):
    
    trains = Train.objects.all()
    
    
    context = {
        "trains": trains,
    }
    
    return render(request, 'web/train-seat.html', context=context)
    

 
 
