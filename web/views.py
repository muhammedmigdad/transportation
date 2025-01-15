from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from users.models import User
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db.models import Q


@login_required(login_url='/login/')
def seat_selection(request, id):
    bus = Bus(id=id)

    if request.method == "POST":
        # selected_seat_ids = request.POST.get('selected_seats', '').split(',')

        # seats = BusSeatStatus.objects.filter(buses=bus, id__in=selected_seat_ids)

        # for seat in seats:
        #     if seat.status != 'booked':
        #         seat.status = 'booked'
        #         seat.save()

        # return JsonResponse({"message": "Seats booked successfully!"}, status=200)
        pass

    seats = BusSeatStatus.objects.filter(buses=bus)
    print(seats)

    context = {
        "bus": bus, 
        "seats": seats,
    }
    return render(request, 'web/bus-seat.html', context)




@login_required(login_url='/login/')
def index(request):
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    flights = Flight.objects.all()
    airlineses = Airlines.objects.all()

    departure_name = request.GET.get('from', '').strip()
    arrival_name = request.GET.get('to', '').strip()
    travel_date = request.GET.get('date', None)

    if departure_name:
        flights = flights.filter(departure_name__icontains=departure_name)
    if arrival_name:
        flights = flights.filter(arrival_name__icontains=arrival_name)
    if travel_date:
        try:
            travel_date_obj = datetime.strptime(travel_date, "%Y-%m-%d").date()
            today_date = datetime.now().date()

            if travel_date_obj >= today_date:
                flights = flights.filter(date=travel_date)
            else:
                flights = flights.none()
        except ValueError:
            flights = flights.none()

    context = {
        'categories': categories,
        'sliders': sliders,
        'flights': flights,
        'airlineses': airlineses,
    }

    if departure_name or arrival_name or travel_date:
        return render(request, "web/flight.html", context=context)

    return render(request, "web/index.html", context=context)




@login_required(login_url='/login/')
def flight(request):
    # Define constants for filters
    PRICE_RANGES = {
        '3000-200000': (3000, 200000),
        '3000-5000': (3000, 5000),
        '10000-25000': (10000, 25000),
        '25000-40000': (25000, 40000),
        '40000-60000': (40000, 60000),
        '60000-80000': (60000, 80000),
        '80000-100000': (80000, 100000),
        '100000-200000': (100000, 200000),
    }

    STOP_OPTIONS = {
        'Non Stop': 'Non-stop',
        'one Stop': '1 stop',
    }

    SORT_OPTIONS = {
        'latest': '-created_on',
        'high-low': '-price',
        'low-high': 'price',
        'Faster': 'duration',
    }

    # Initialize data
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    flights = Flight.objects.all()
    airlineses = Airlines.objects.all()

    # Apply filters
    selected_airline = request.GET.get('category', None)
    if selected_airline and selected_airline != 'all':
        flights = flights.filter(airline__name=selected_airline)

    selected_stop = request.GET.get('Stop', None)
    if selected_stop in STOP_OPTIONS:
        flights = flights.filter(stops=STOP_OPTIONS[selected_stop])

    price = request.GET.get('price', None)
    if price in PRICE_RANGES:
        flights = flights.filter(price__range=PRICE_RANGES[price])

    departure_name = request.GET.get('from', '').strip()
    arrival_name = request.GET.get('to', '').strip()
    travel_date = request.GET.get('date', None)

    if departure_name:
        flights = flights.filter(departure_name__icontains=departure_name)
    if arrival_name:
        flights = flights.filter(arrival_name__icontains=arrival_name)
    if travel_date:
        try:
            travel_date_obj = datetime.strptime(travel_date, "%Y-%m-%d").date()
            if travel_date_obj >= datetime.now().date():
                flights = flights.filter(date=travel_date)
            else:
                flights = flights.none()
        except ValueError:
            flights = flights.none()

    # Apply sorting
    sort_option = request.GET.get('sort', 'default')
    if sort_option in SORT_OPTIONS:
        flights = flights.order_by(SORT_OPTIONS[sort_option])



    # Prepare context
    context = {
        'categories': categories,
        'sliders': sliders,
        'flights': flights,
        'airlineses': airlineses,
    }

    return render(request, "web/flight.html", context=context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('web:index'))
        else:
            context = {
                'error': True,
                'message': 'Invalid Email or Password'
            }
            return render(request, 'web/login.html', context=context)
    
    return render(request, 'web/login.html')
    
def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_valid': User.objects.filter(email__iexact=email).exists()
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
                'message': 'Email Already Exists'
            }
            return render(request, 'web/register.html', context=context)
        
        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()

        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.save()

        return HttpResponseRedirect(reverse('web:login'))

    return render(request, 'web/register.html')
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('web:login'))


@login_required(login_url='/login/')
def train_search(request):
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    trains = Train.objects.all()
    trainses = Trains.objects.all()
    price = request.GET.get('price')
    selected_trainses = request.GET.get('category', 'all')
    selected_stop = request.GET.get('Stop', '')
    selected_train = request.GET.get('train', None)
    price_min = request.GET.get('price_min', None)
    price_max = request.GET.get('price_max', None)
    
    if selected_train and selected_train != 'all':
        trains = trains.filter(train__name=selected_train)

    if price_min and price_max:
        trains = trains.filter(price__range=(price_min, price_max))

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
        
    departure_name = request.GET.get('from', '').strip()
    arrival_name = request.GET.get('to', '').strip()
    travel_date = request.GET.get('date', None)

    # Apply filters
    if departure_name:
        trains = trains.filter(departure_name__icontains=departure_name)
    if arrival_name:
        trains = trains.filter(arrival_name__icontains=arrival_name)
    if travel_date:
        trains = trains.filter(date=travel_date)

    
    
    context = {
        'categories': categories,
        'sliders': sliders,
        "trains": trains,
        "trainses": trainses,
    }
    return render(request, 'web/train-search.html', context=context)

@login_required(login_url='/login/')
def train(request):
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    trains = Train.objects.all()
    trainses = Trains.objects.all()
    
        
    departure_name = request.GET.get('from', '').strip()
    arrival_name = request.GET.get('to', '').strip()
    travel_date = request.GET.get('date', None)

    if departure_name:
        trains = trains.filter(departure_name__icontains=departure_name)
    if arrival_name:
        trains = trains.filter(arrival_name__icontains=arrival_name)
    if travel_date:
        trains = trains.filter(date=travel_date)

    
    
    context = {
        'categories': categories,
        'sliders': sliders,
        "trains": trains,
        "trainses": trainses,
    }
    if departure_name or arrival_name or travel_date:
        return render(request, "web/train-search.html", context=context)
    
    return render(request, 'web/train.html', context=context)

@login_required(login_url='/login/')
def bus_search(request):
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    bus = Bus.objects.all()
    buses = Buses.objects.all()
    price = request.GET.get('price')
    selected_bus = request.GET.get('category', 'all')
    selected_stop = request.GET.get('Stop', '')
    selected_bus = request.GET.get('bus', None)
    price_min = request.GET.get('price_min', None)
    price_max = request.GET.get('price_max', None)
    
    if selected_bus and selected_bus != 'all':
        bus = bus.filter(bus__name=selected_bus)

    if price_min and price_max:
        bus = bus.filter(price__range=(price_min, price_max))

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
        
    departure_name = request.GET.get('from', '').strip()  
    arrival_name = request.GET.get('to', '').strip()    
    travel_date = request.GET.get('date', None)  

    if departure_name:
        bus = bus.filter(departure_name__icontains=departure_name)  
    if arrival_name:
        bus = bus.filter(arrival_name__icontains=arrival_name) 
    if travel_date:
        bus = bus.filter(date=travel_date)  

    
    context = {
        'categories': categories,
        'sliders': sliders,
        "bus": bus,
        "buses": buses
    }
    return render(request, 'web/bus-search.html', context=context)
@login_required(login_url='/login/')
def bus(request):
    categories = Category.objects.all()
    sliders = Slider.objects.all()
    bus = Bus.objects.all()
    buses = Buses.objects.all()
        
    departure_name = request.GET.get('from', '').strip()  
    arrival_name = request.GET.get('to', '').strip()    
    travel_date = request.GET.get('date', None)  

    if departure_name:
        bus = bus.filter(departure_name__icontains=departure_name)  
    if arrival_name:
        bus = bus.filter(arrival_name__icontains=arrival_name) 
    if travel_date:
        bus = bus.filter(date=travel_date)  

    
    context = {
        'categories': categories,
        'sliders': sliders,
        "bus": bus,
        "buses": buses
    }
    
    if departure_name or arrival_name or travel_date:
        return render(request, "web/bus-search.html", context=context)
    
    return render(request, 'web/bus.html', context=context)


@login_required(login_url='/login/')
def flight_books(request):


    return render(request, 'web/flight-books.html')



@login_required(login_url='/login/')
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
        cartbill.tax_charge = 50.00 
        cartbill.totel_amount = trains.price + 50  
        cartbill.offer_amount = 0.00 
        cartbill.save()
    else:
        cartbill = CartBill.objects.create(
            customer=customer,
            item_total=float(trains.price), 
            tax_charge=50.00, 
            totel_amount=trains.price + 50,  
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
            baggage_allowance='Per Traveller',
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



@login_required(login_url='/login/')
def bus_books(request, id):  
    user = request.user
    customer = Customer.objects.get(user=user)
    buses = Bus.objects.get(id=id)
    if CartBill.objects.filter(customer=customer).exists():
        cartbill = CartBill.objects.get(customer=customer)
        cartbill.item_total = float(buses.price)  
        cartbill.tax_charge = 70.00 
        cartbill.totel_amount = buses.price + 70  
        cartbill.offer_amount = 0.00 
        cartbill.save()
    else:
        cartbill = CartBill.objects.create(
            customer=customer,
            item_total=float(buses.price), 
            tax_charge=70.00, 
            totel_amount=buses.price + 70,  
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
            baggage_allowance='Per Traveller ',
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



@login_required(login_url='/login/')
def bus_seat(request):
    
    bus = Bus.objects.all()
    
    
    context = {
        "bus": bus,
    }
    
    return render(request, 'web/bus-seat.html', context=context)


@login_required(login_url='/login/')
def train_seat(request):
    
    trains = Train.objects.all()
    
    
    context = {
        "trains": trains,
    }
    
    return render(request, 'web/train-seat.html', context=context)


 
 
@login_required(login_url='/login/')
def flight_class(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)

    try:
        flight = Flight.objects.get(id=id)
    except Flight.DoesNotExist:
        return redirect('flight_not_found')
    
    
    travel_class_prices = TravelClassPrice.objects.filter(
        airline=flight.airline,
    )

    if request.method == 'POST':
        adults = int(request.POST.get('adults', 1))
        children = int(request.POST.get('children', 0))
        infants = int(request.POST.get('infants', 0))
        travel_class = request.POST.get('travel-class', 'economy')

        try:
            selected_class = travel_class_prices.get(travel_class=travel_class)
            travel_class_price = float(selected_class.price)
        except TravelClassPrice.DoesNotExist:
            travel_class_price = 0.0

        total_price = (adults + children + infants) * travel_class_price
        tax_rate = 10.0
        tax_charge = round((tax_rate / 100) * total_price, 2)

        cartbill, created = CartBill.objects.get_or_create(
            customer=customer,
            defaults={
                'item_total': total_price,
                'tax_charge': tax_charge,
                'totel_amount': total_price + tax_charge,
                'offer_amount': 0.00,
                'adults': adults,
                'children': children,
                'infants': infants,
            }
        )

        if not created:
            cartbill.item_total = total_price
            cartbill.tax_charge = tax_charge
            cartbill.totel_amount = total_price + tax_charge
            cartbill.offer_amount = 0.00
            cartbill.adults = adults
            cartbill.children = children
            cartbill.infants = infants
            cartbill.save()

        flightbill, created = FlightBill.objects.get_or_create(
            fligths=flight,customer=customer,
            defaults={
                'airline_name': flight.airline.name,  
                'flight_code': flight.flight_numbers,
                'departure_time': flight.departure_time,
                'arrival_time': flight.arrival_time,
                'duration': flight.duration,
                'departure_airport': flight.departure_code,
                'arrival_airport': flight.arrival_code,
                'baggage_allowance': 'Per Traveller',
                'cabin_baggage': '7 Kg',
                'check_in_baggage': '20 Kg',
                'terminal': 'IN',
                'status': '70% On-time',
                'travel_class_price': total_price     
            }
        )

        if not created:
            flightbill.airline_name = flight.airline.name
            flightbill.flight_code = flight.flight_numbers
            flightbill.departure_time = flight.departure_time
            flightbill.arrival_time = flight.arrival_time
            flightbill.duration = flight.duration
            flightbill.departure_airport = flight.departure_code
            flightbill.arrival_airport = flight.arrival_code
            flightbill.price = total_price 
            flightbill.save()

        error_message = None
        success_message = None
        code = request.POST.get('code')
        if code:
            try:
                offer = Offer.objects.get(code=code)

                if cartbill.offer_code == code:
                    error_message = 'Coupon code has already been applied!'
                else:
                    if offer.is_percentage:
                        discount = round((offer.discount / 100) * cartbill.item_total, 2)
                    else:
                        discount = offer.discount
                    discount = min(discount, cartbill.item_total)

                    cartbill.offer_amount = discount
                    cartbill.totel_amount = cartbill.item_total + cartbill.tax_charge - discount
                    cartbill.offer_code = code 
                    cartbill.save()

                    success_message = 'Coupon code applied successfully!'
            except Offer.DoesNotExist:
                error_message = 'Invalid coupon code. Please try again.'


        context = {
            "flight": flight,
            "cartbill": cartbill,
            "flightbill": flightbill,
            "travel_class_prices": travel_class_prices,
            "error_message": error_message,
            "success_message": success_message,
            "adults": adults,
            "children": children,
            "infants": infants,
            "travel_class": travel_class,
        }
        return render(request, "web/flight-books.html", context)

    context = {
        "flight": flight,
        "travel_class_prices": travel_class_prices,
    }
    return render(request, "web/flight-class.html", context)


@login_required(login_url='/login/')
def flight_details(request):

    return render(request, "web/flight-details.html")

