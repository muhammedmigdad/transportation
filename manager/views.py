from django.shortcuts import render, reverse, redirect
from web.models import *
from django.http import HttpResponseRedirect, HttpResponse
from manager.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from main.functions import generate_form_errors
from main.decorators import allow_manager


@allow_manager
@login_required(login_url='/login/')
def index(request):
    
    return render(request,'manager/index.html')

def login(request):
    if request.method == "POST":
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_manager: 
                    auth_login  (request,user)
                    return redirect('manager:index') 
                else:
                    messages.error(request, "Unauthorized access.")
                    return HttpResponse("unauthorized", status=401)
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Form is invalid.")
    else:
        form = ManagerLoginForm()

    return render(request, 'manager/login.html', {'form': form})


def logout(request):
    return redirect('manager:login')


@allow_manager
@login_required(login_url='/login/')
def slider(request):
    instances = Slider.objects.all()
    
    context = {
        'instances': instances,
    }
    
    
    return render(request,'manager/slider.html', context=context)
@allow_manager
@login_required(login_url='/login/')

def slider_delete(request,id):
    instance = Slider.objects.get(id=id)
    
    instance.delete()
    
    return HttpResponseRedirect(reverse('manager:slider'))
@allow_manager
@login_required(login_url='/login/')
def slider_add(request,):
    if request.method == 'POST':   
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:slider'))
            
        else:
            message = generate_form_errors(form)
            form = SliderForm()

            context = {
            "error": True,
            "message": message,
            "form": form,
            }
    
        return render(request,'manager/slider_add.html', context=context)



    else:
        form = SliderForm()
        
        context = {
            "form": form,
        }
        
    return render(request,'manager/slider_add.html', context=context)
@allow_manager
@login_required(login_url='/login/')
def slider_edit(request,id):
    instance = Slider.objects.get(id=id)
    if request.method == 'POST':   
        form = SliderForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:slider'))
            
        else:
            message = generate_form_errors(form)
            form = SliderForm()

            context = {
            "error": True,
            "message": message,
            "form": form,
            "instance": instance
            }
    
        return render(request,'manager/slider_add.html', context=context)



    else:
        form = SliderForm(instance=instance)
        
        context = {
            "form": form,
            "instance": instance
        }
        
    return render(request,'manager/slider_add.html', context=context)



@allow_manager
@login_required(login_url='/login/')
def users(request):
    instances = User.objects.all()
    
    context = {
        'instances': instances,
    }
    
    return render(request,'manager/users.html', context=context)

@allow_manager
@login_required(login_url='/login/')

def users_delete(request, id):
    instance = User.objects.get(id=id)
    
    instance.delete()
    
    return HttpResponseRedirect(reverse('manager:users'))
@allow_manager
@login_required(login_url='/login/')

def users_add(request):
    if request.method == 'POST':   
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:users'))
        else:
            message = generate_form_errors(form)
            form = UserForm()

            context = {
                "error": True,
                "message": message,
                "form": form,
            }
    
        return render(request, 'manager/users_add.html', context=context)
    else:
        form = UserForm()
        
        context = {
            "form": form,
        }
        
    return render(request, 'manager/users_add.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def users_edit(request, id):
    instance = User.objects.get(id=id)
    if request.method == 'POST':   
        form = UserForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:users'))
            
        else:
            message = generate_form_errors(form)
            form = UserForm()

            context = {
            "error": True,
            "message": message,
            "form": form,
            "instance": instance
            }
    
        return render(request,'manager/users_add.html', context=context)



    else:
        form = UserForm(instance=instance)
        
        context = {
            "form": form,
            "instance": instance
        }
        
    return render(request,'manager/users_add.html', context=context)


@allow_manager
@login_required(login_url='/login/')
def offers(request):
    instances = Offer.objects.all()
    
    context = {
        'instances': instances,
    }
    
    return render(request,'manager/offers.html', context=context)

@allow_manager
@login_required(login_url='/login/')

def offers_delete(request, id):
    instance = Offer.objects.get(id=id)
    
    instance.delete()
    
    return HttpResponseRedirect(reverse('manager:offers'))
@allow_manager
@login_required(login_url='/login/')
def offers_add(request):
    if request.method == 'POST':   
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:offers'))
        else:
            message = generate_form_errors(form)
            form = OfferForm()

            context = {
                "error": True,
                "message": message,
                "form": form,
            }
    
        return render(request, 'manager/offers_add.html', context=context)
    else:
        form = OfferForm()
        
        context = {
            "form": form,
        }
        
    return render(request, 'manager/offers_add.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def offers_edit(request, id):
    instance = Offer.objects.get(id=id)
    if request.method == 'POST':   
        form = OfferForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:offers'))
            
        else:
            message = generate_form_errors(form)
            form = OfferForm()

            context = {
            "error": True,
            "message": message,
            "form": form,
            "instance": instance
            }
    
        return render(request,'manager/offers_add.html', context=context)



    else:
        form = OfferForm(instance=instance)
        
        context = {
            "form": form,
            "instance": instance
        }
        
    return render(request,'manager/offers_add.html', context=context)


@allow_manager
@login_required(login_url='/login/')
def flight(request):
    instances = Flight.objects.all()
    
    context = {
        'instances': instances,
    }
    
    
    return render(request,'manager/flight.html', context=context)
@allow_manager
@login_required(login_url='/login/')

def flight_delete(request,id):
    
    instance = Flight.objects.get(id=id)
    
    instance.delete()
    
    return HttpResponseRedirect(reverse('manager:flight'))
@allow_manager
@login_required(login_url='/login/')
def flight_add(request,):
    if request.method == 'POST':   
        form = FlightForm(request.POST, request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:flight'))
            
        else:
            message = generate_form_errors(form)
            form = FlightForm()

            context = {
            "error": True,
            "message": message,
            "form": form,
            }
    
        return render(request,'manager/flight_add.html', context=context)



    else:
        form = FlightForm()
        
        context = {
            "form": form,
        }
        
    return render(request,'manager/flight_add.html', context=context)
@allow_manager
@login_required(login_url='/login/')
def flight_edit(request,id):
    instance = Flight.objects.get(id=id)
    if request.method == 'POST':   
        form = FlightForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:flight'))
            
        else:
            message = generate_form_errors(form)
            form = FlightForm()

            context = {
            "error": True,
            "message": message,
            "form": form,
            "instance": instance
            }
    
        return render(request,'manager/flight_add.html', context=context)



    else:
        form = FlightForm(instance=instance)
        
        context = {
            "form": form,
            "instance": instance
        }
        
    return render(request,'manager/flight_add.html', context=context)



@allow_manager
@login_required(login_url='/login/')
def bus(request):
    instances = Bus.objects.all()
    
    context = {
        'instances': instances,
    }
    
    
    return render(request,'manager/bus.html', context=context)
@allow_manager
@login_required(login_url='/login/')

def bus_delete(request,id):
    
    instance = Bus.objects.get(id=id)
    
    instance.delete()
    
    return HttpResponseRedirect(reverse('manager:bus'))
@allow_manager
@login_required(login_url='/login/')
def bus_add(request,):
    if request.method == 'POST':   
        form = BusForm(request.POST, request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:bus'))
            
        else:
            message = generate_form_errors(form)
            form = BusForm()

            context = {
            "error": True,
            "message": message,
            "form": form,
            }
    
        return render(request,'manager/bus_add.html', context=context)


    else:
        form = BusForm()
        
        context = {
            "form": form,
        }
        
    return render(request,'manager/bus_add.html', context=context)
@allow_manager
@login_required(login_url='/login/')
def bus_edit(request,id):
    instance = Bus.objects.get(id=id)
    if request.method == 'POST':   
        form = BusForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:bus'))
            
        else:
            message = generate_form_errors(form)
            form = BusForm()

            context = {
            "error": True,
            "message": message,
            "form": form,
            "instance": instance
            }
    
        return render(request,'manager/bus_add.html', context=context)



    else:
        form = BusForm(instance=instance)
        
        context = {
            "form": form,
            "instance": instance
        }
        
    return render(request,'manager/bus_add.html', context=context)


@allow_manager
@login_required(login_url='/login/')
def train(request):
    instances = Train.objects.all()
    
    context = {
        'instances': instances,
    }
    return render(request,'manager/train.html', context=context)
@allow_manager
@login_required(login_url='/login/')
def train_delete(request,id):
    instance = Train.objects.get(id=id)
    
    instance.delete()
    
    return HttpResponseRedirect(reverse('manager:train'))
@allow_manager
@login_required(login_url='/login/')
def train_add(request):
    if request.method == 'POST':   
        form = TrainForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse('manager:train'))

        else:
            message = generate_form_errors(form)
            form = TrainForm()

            context = {
                "error": True,
                "message": message,
                "form": form,
            }
        return render(request, 'manager/train_add.html', context=context)
    else:
        form = TrainForm()
        
        context = {
            "form": form,
        }
        
    return render(request, 'manager/train_add.html', context=context)
@allow_manager
@login_required(login_url='/login/')
def train_edit(request,id):
    instance = Train.objects.get(id=id)
    if request.method == 'POST':   
        form = TrainForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:train'))
            
        else:
            message = generate_form_errors(form)
            form = TrainForm()

            context = {
            "error": True,
            "message": message,
            "form": form,
            "instance": instance
            }
    
        return render(request,'manager/train_add.html', context=context)



    else:
        form = TrainForm(instance=instance)
        
        context = {
            "form": form,
            "instance": instance
        }
        
    return render(request,'manager/train_add.html', context=context)