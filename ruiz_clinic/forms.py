from django import forms
from .models import *
from django.core.exceptions import ValidationError
from datetime import time


#_________________________________IVENTORY___________________________________________________
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_brand','item_model','item_price','item_date_in','item_quantity','item_color','item_measurement','item_category_id','item_frame_type_id',
        ]
        widgets = {
            'item_brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item brand'}),
            'item_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item model'}),
            'item_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'item_date_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'item_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'item_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter color'}),
            'item_measurement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter measurements'}),
            'item_category_id': forms.Select(attrs={'class': 'form-control'}),
            'item_frame_type_id': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'item_brand': 'Brand',
            'item_model': 'Model',
            'item_price': 'Price',
            'item_date_in': 'Date In',
            'item_quantity': 'Quantity',
            'item_color': 'Color',
            'item_measurement': 'Measurement',
            'item_category_id': 'Category',
            'item_frame_type_id': 'Frame Type',
        }

#_____________________________________PATIENT__________________________________________________
class PatientForm(forms.ModelForm):
    pass

#_________________________________APPOINTMENT___________________________________________________
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['app_fname', 'app_lname', 'app_contact', 'app_date', 'app_time']  # Exclude 'app_status'
        widgets = {
            'app_date': forms.DateInput(attrs={'type': 'date'}),
            'app_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'app_fname': 'First Name',
            'app_lname': 'Last Name',
            'app_contact': 'Contact Number',
            'app_date': 'Date',
            'app_time': 'Time',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If an initial date is passed, populate the `app_date` field
        if 'initial' in kwargs and 'app_date' in kwargs['initial']:
            self.fields['app_date'].initial = kwargs['initial']['app_date']
