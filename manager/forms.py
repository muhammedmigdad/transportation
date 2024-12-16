from django import forms
from web.models import *
from users.models import User


class ManagerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    
    
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'is_customer', 'is_store', 'is_agent', 'is_manager']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'is_customer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_store': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_agent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SliderForm(forms.ModelForm):  
    class Meta:
        model = Slider
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slider Name'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['code', 'discount', 'short_description', 'is_percentage']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Offer Code'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount Amount'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short Description'}),
            'is_percentage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['image', 'airline', 'flight_numbers', 'departure_time',  'departure_code','duration', 'stops', 'arrival_time', 'arrival_code','price','discount']
        widgets = {
            'flight_numbers': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter flight number' }),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time' }),
            'departure_code': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter departure code'}),
            'arrival_code': forms.TextInput(attrs={ 'class': 'form-control','placeholder': 'Enter arrival code' }),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter price' }),
            'discount': forms.NumberInput(attrs={ 'class': 'form-control','placeholder': 'Enter discount (optional)'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'stops': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter number of stops' }),
            'duration': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter duration (e.g., 2:30:00)' }),
        }
        
class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['image', 'buses', 'bus_numbers', 'departure_time',  'departure_code','duration', 'stops', 'arrival_time', 'arrival_code','price','discount']
        widgets = {
            'bus_numbers': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter bus number' }),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time' }),
            'departure_code': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter departure code'}),
            'arrival_code': forms.TextInput(attrs={ 'class': 'form-control','placeholder': 'Enter arrival code' }),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter price' }),
            'discount': forms.NumberInput(attrs={ 'class': 'form-control','placeholder': 'Enter discount (optional)'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'stops': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter number of stops' }),
            'duration': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter duration (e.g., 2:30:00)' }),
        }
        
        
class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['image', 'trains', 'train_numbers', 'departure_time',  'departure_code','duration', 'stops', 'arrival_time', 'arrival_code','price','discount']
        widgets = {
            'train_numbers': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter train number' }),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time' }),
            'departure_code': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter departure code'}),
            'arrival_code': forms.TextInput(attrs={ 'class': 'form-control','placeholder': 'Enter arrival code' }),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter price' }),
            'discount': forms.NumberInput(attrs={ 'class': 'form-control','placeholder': 'Enter discount (optional)'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'stops': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter number of stops' }),
            'duration': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter duration (e.g., 2:30:00)' }),
        }