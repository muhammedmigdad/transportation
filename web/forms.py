from django import forms
from .models import BusSeat

class SeatBookingForm(forms.Form):
    seat_ids = forms.CharField(widget=forms.HiddenInput())
