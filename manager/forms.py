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
