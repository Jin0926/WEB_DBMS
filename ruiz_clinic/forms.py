from django import forms
from .models import *
from django.core.exceptions import ValidationError
from datetime import time



#_________________________________IVENTORY___________________________________________________
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_brand','item_model','item_price','item_date_in',
                  'item_quantity','item_color','item_measurement',
                  'item_category_id','item_frame_type_id',
        ]

        widgets = {
            'item_brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item brand'}),
            'item_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item model'}),
            'item_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'item_date_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'item_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'item_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter color'}),
            'item_measurement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter measurement (Optional)'}),
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
            'item_category_id': 'Category(Optional)',
            'item_frame_type_id': 'Frame Type',
        }

#_____________________________________PATIENT__________________________________________________
class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = [
            'patient_fname', 'patient_lname', 'patient_initial', 
            'patient_address', 'patient_occupation', 
            'patient_date_checked_up','patient_birthdate', 'patient_contact','patient_diag'
        ]
        widgets = {
            'patient_fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'patient_lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'patient_initial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter initial'}),
            'patient_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'patient_occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter occupation(Optional)'}),
            'patient_date_checked_up': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'patient_birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'patient_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'patient_diag': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Diagnosed with..'}),
            
        }
        labels = {
            'patient_fname': 'First Name',
            'patient_lname': 'Last Name',
            'patient_initial': 'Initial',
            'patient_address': 'Address',
            'patient_occupation': 'Occupation',
            'patient_date_checked_up': 'Date Checked Up',
            'patient_birthdate': 'Birthdate',
            'patient_contact': 'Contact',
            'patient_diag': 'Diagnosed',  
        }

    def clean_patient_date_checked_up(self):
        date = self.cleaned_data['patient_date_checked_up']
        if date > now().date():
            raise ValidationError("Check-up date cannot be in the future")
        return date


class PurchasedItemForm(forms.ModelForm):
    item_price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'placeholder': 'Price will appear here'}),
        label='Item Price'
    )

    class Meta:
        model = Purchased_Item
        fields = ['item_code', 'patient_id']  # Exclude payment_id
        widgets = {
            'item_code': forms.Select(attrs={'class': 'form-control'}),
            'patient_id': forms.HiddenInput(),
        }
        labels = {
            'item_code': 'Item',
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)  # Ensure the patient is passed to the form
        super().__init__(*args, **kwargs)

        if patient:
            self.fields['patient_id'].initial = patient.patient_id  # Set the patient_id field value dynamically



class ItemPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_payed', 'payment_to_be_payed', 'payment_method', 'payment_terms']

        widgets = {
            'payment_payed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount Paid'}),
            'payment_to_be_payed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Amount'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_terms': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'payment_payed': 'Amount Paid',
            'payment_to_be_payed': 'Total Amount to Pay',
            'payment_method': 'Payment Method',
            'payment_terms': 'Payment Terms',
        }

    def clean(self):
        cleaned_data = super().clean()
        payment_payed = cleaned_data.get('payment_payed')
        payment_to_be_payed = cleaned_data.get('payment_to_be_payed')

        if payment_payed is not None and payment_to_be_payed is not None:
            if payment_payed > payment_to_be_payed:
                raise ValidationError("Paid amount cannot exceed the total amount to be paid.")
        
        return cleaned_data

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




