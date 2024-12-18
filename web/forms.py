from django import forms
from .models import BusSeatStatus


class BusSeatStatusForm(forms.ModelForm):
    class Meta:
        model = BusSeatStatus
        fields = ['seat_side', 'seat_number', 'status', 'buses']

    def clean_seat_number(self):
        seat_number = self.cleaned_data.get('seat_number')
        if seat_number <= 0:
            raise forms.ValidationError("Seat number must be a positive integer.")
        return seat_number

