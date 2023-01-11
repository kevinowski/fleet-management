from django import forms
from django.core.exceptions import ValidationError

from .models import Car, Refuel, Service


class AddCarForm(forms.ModelForm):
    
    class Meta:
        model = Car
        exclude = ("slug", "last_service")


class RefuelForm(forms.ModelForm):

    class Meta:
        model = Refuel
        fields = ("car", "mileage", "liters", "city")

    def clean_mileage(self):
        car = self.cleaned_data['car']
        new_mileage = self.cleaned_data['mileage']
        if new_mileage <= car.mileage:
            raise ValidationError(f"Mileage must be greater than {car.mileage} km.")
        car.mileage = new_mileage
        car.save()
        return new_mileage
   

class ServiceForm(forms.ModelForm):
    service_type = forms.ChoiceField(choices=[["OIL", "OIL"], ["TYRES", "TYRES"], ["MALFUNCTION", "MALFUNCTION"]],)
    
    class Meta:
        model = Service
        fields = ("car", "service_type", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False

    
        
