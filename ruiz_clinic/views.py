
from django.utils import timezone   
from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from datetime import datetime
from django.http import HttpResponse, JsonResponse,Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q
import json


#_____________________________________DASHBOARD__________________________________________________________
def dashboard(request):
    # Get the selected date from the request or default to today
    selected_date_str = request.GET.get('selected_date')
    if selected_date_str:
        try:
            selected_date = timezone.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.localdate()
    else:
        selected_date = timezone.localdate()

    # Filter appointments for the selected date
    appointments = Appointment.objects.filter(app_date=selected_date).order_by('app_time')

    # Query for items with quantity less than 5
    low_stock_items = Item.objects.filter(item_quantity__lt=3)

    return render(request, 'clinic/Dashboard/dashboard.html', {
        'appointments': appointments,
        'selected_date': selected_date,  # Pass the selected date to the template
        'low_stock_items': low_stock_items,  # Pass the low stock items to the template
    })


@csrf_exempt
def update_appointment_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            appointment_id = data.get('appointment_id')  # ID passed from frontend
            next_status = data.get('next_status')  # Next status to update

            # Retrieve the appointment using the correct field name
            appointment = Appointment.objects.get(app_id=appointment_id)
            appointment.app_status = next_status
            appointment.save()

            return JsonResponse({'success': True, 'new_status': next_status})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    

#_____________________________________APPOINTMENT__________________________________________________________

def appointment(request):
    # Fetch all appointment dates from the database
    appointments = Appointment.objects.all().values('app_date')

    # Convert to datetime and adjust for time zone
    appointment_dates = [
        (datetime.combine(appointment['app_date'], datetime.min.time())  # Combine date with a dummy time
         .astimezone(timezone.get_current_timezone()).date().isoformat())  # Convert to local time zone and then to string
        for appointment in appointments
    ]

    context = {
        'appointment_dates': appointment_dates,  # Pass the dates to the template
    }
    return render(request, 'clinic/Appointment/appointment.html', context)

def view_appointment(request):
    # Retrieve query parameters
    date_str = request.GET.get('date')  # Get the selected date from the query parameters
    search_query = request.GET.get('search', '')  # Optional search query for filtering
    
    selected_date = None
    formatted_date = "Unknown Date"
    appointments = []
    is_past_date = False
    is_past_time = False
    is_sunday = False

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d")  # Convert to a datetime object
            formatted_date = selected_date.strftime("%B %d, %Y")  # Format the date as 'Month Day, Year'

            # Get today's date and time
            now = datetime.now()
            current_time = now.time()

            # Check if the selected date is in the past
            if selected_date.date() < now.date():  # Compare only the date part
                is_past_date = True
            elif selected_date.date() == now.date():
                # Check if the current time is outside business hours (8:00 AM - 5:00 PM)
                start_time = datetime.strptime("08:00", "%H:%M").time()
                end_time = datetime.strptime("17:00", "%H:%M").time()

                if current_time < start_time or current_time > end_time:
                    is_past_time = True

            # Check if the selected date is a Sunday
            if selected_date.weekday() == 6:  # 6 represents Sunday
                is_sunday = True

            # Get all appointments for the selected date
            appointments = Appointment.objects.filter(app_date=selected_date)

            # Apply the search filter if a search query is provided
            if search_query:
                appointments = appointments.filter(
                    app_fname__icontains=search_query  # Adjust based on searchable fields
                )

            # Sort by appointment time
            appointments = appointments.order_by('app_time')

            # Add a flag to each appointment to indicate if it occurs in the past
            for appointment in appointments:
                appointment_time = datetime.combine(selected_date, appointment.app_time)
                appointment.is_past = appointment_time < now  # Compare with the current datetime

        except ValueError:
            pass  # Handle invalid date strings gracefully

    # Create the form instance and pass the selected date to the form's `app_date` field
    form = AppointmentForm(initial={'app_date': selected_date})

    context = {
        'formatted_date': formatted_date,  # Pass the formatted date
        'selected_date': selected_date,   # Optionally, pass the raw datetime object
        'appointments': appointments,      # Pass the sorted appointments to the template
        'form': form,                      # Pass the form to the template
        'is_past_date': is_past_date,      # Flag to check if it's a past date
        'is_past_time': is_past_time,      # Flag to check if it's a past time for today
        'is_sunday': is_sunday,            # Pass the is_sunday flag to the template
        'search_query': search_query,      # Pass the search query to the template
    }

    return render(request, 'clinic/Appointment/view_appointment.html', context)

def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.app_status = 'Waiting'  # Set default status to Waiting
            appointment.save()
            # Redirect to the same date's view after creation
            return redirect(f"{reverse('view_appointment')}?date={form.cleaned_data['app_date']}")
    else:
        form = AppointmentForm()

    return render(request, 'clinic/Appointment/create_appointment.html', {'form': form})

def edit_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

        # Ensure appointment_id is provided and valid
        if not appointment_id:
            messages.error(request, "Appointment ID is missing.")
            return redirect('view_appointment')

        # Fetch the appointment or return 404 if not found
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        form = AppointmentForm(request.POST, instance=appointment)

        # If the form is valid, save the changes and provide success feedback
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully.")
            # Redirect to the `view_appointment` page, passing the updated date to the query string
            return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")
        else:
            messages.error(request, "Invalid form submission.")
            return redirect('view_appointment')

    return redirect('view_appointment')  # Fallback for non-POST requests

@csrf_exempt
def delete_appointment(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            appointment_id = data.get('appointment_id')

            if not appointment_id:
                return JsonResponse({'success': False, 'error': 'Appointment ID is missing'})

            # Retrieve and delete the appointment
            appointment = get_object_or_404(Appointment, pk=appointment_id)
            appointment.delete()

            # Include a success message for the front-end
            return JsonResponse({'success': True, 'message': 'Appointment deleted successfully'})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

#_____________________________________INVENTORY__________________________________________________________

def inventory(request):
    items = Item.objects.all()  # Fetch all items from the database
    return render(request, 'clinic/Inventory/inventory.html', {'items': items})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')  
    else:
        form = ItemForm()
    return render(request, 'clinic/Inventory/add_item.html', {'form': form})

def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)  # Fetch the item by id
    if request.method == 'POST': 
        item.delete()  
        return redirect('inventory')  
    return redirect('inventory') 

def view_item(request, item_id):
    # Fetch the item by its ID
    item = get_object_or_404(Item, pk=item_id)

    # Get all purchases of this item (if any)
    purchased_items = Purchased_Item.objects.filter(item_code=item)

    # Prepare patient details
    patient_details = []
    for purchased_item in purchased_items:
        patient_name = f"{purchased_item.patient_id.patient_fname} {purchased_item.patient_id.patient_lname}"
        date_out = item.item_date_out  # Assuming item date_out should be shown for all purchased items
        patient_details.append({
            'patient_name': patient_name,
            'date_out': date_out,
            'pur_date_purchased': purchased_item.pur_date_purchased,
        })

    # Pass these details to the template
    context = {
        'item': item,
        'patient_details': patient_details,  # List of patient details
    }

    return render(request, 'clinic/Inventory/view_item.html', context)


#_________________________________________PATIENT________________________________________________________

def patient(request):
    patients = Patient.objects.all()
    return render(request, 'clinic/Patient/patient.html', {'patients': patients})

def patient_detail(request, patient_id):
    # Use patient_id instead of id in the query
    patient = get_object_or_404(Patient, patient_id=patient_id)  # Use patient_id here
    
    # Create the form, passing the patient to pre-fill the patient_id field
    form = PurchasedItemForm(request.POST or None, patient=patient)
    
    if form.is_valid():
        form.save()
        # Redirect to a success page or handle the success case
        return redirect('success_url')  # Replace with actual success URL
    
    return render(request, 'clinic/Patient/patient_detail.html', {'patient': patient, 'form': form})

def add_patient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)

        if patient_form.is_valid():
            patient = patient_form.save(commit=False)
            if not patient.patient_date_checked_up:
                patient.patient_date_checked_up = now()
            patient.save()

            messages.success(request, "Patient added successfully!")
            return redirect('patient')
        else:
            messages.error(request, "There was an error adding the patient.")

    else:
        patient_form = PatientForm(initial={'patient_date_checked_up': now()})

    return render(request, 'clinic/Patient/add_patient.html', {
        'patient_form': patient_form,
    })

def delete_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, pk=patient_id)
        patient.delete()
        return redirect('patient')  # Redirect to the patient list after deletion
    return HttpResponse(status=400)

def add_purchased_item(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    purchased_item_form = PurchasedItemForm(request.POST or None, patient=patient)
    payment_form = ItemPaymentForm(request.POST or None)

    if request.method == 'POST':
        if purchased_item_form.is_valid() and payment_form.is_valid():
            purchased_item = purchased_item_form.save(commit=False)
            item = purchased_item.item_code  # Get the item selected for purchase
            
            # Retrieve the item price and set the payment amount
            item_price = item.item_price
            payment = payment_form.save(commit=False)
            payment.payment_to_be_payed = item_price  # Assign the item price as total amount to pay

            # Save payment and purchased item
            payment.save()
            purchased_item.payment_id = payment
            purchased_item.patient_id = patient
            purchased_item.save()

            # Update the 'date out' field for the purchased item
            item.date_out = now()  # Assuming you have a field date_out
            item.save()

            messages.success(request, "Item and payment added successfully!")
            return redirect('patient_detail', patient_id=patient_id)
        else:
            messages.error(request, "There was an error adding the item or payment.")

    return render(request, 'clinic/Patient/patient_bought.html', {
        'purchased_item_form': purchased_item_form,
        'payment_form': payment_form,
        'patient': patient,
    })

def item_search(request):
    query = request.GET.get('q', '').strip()  # Retrieve and strip the search query
    items = Item.objects.filter(
        Q(item_category_id__item_category_name__icontains=query) |  # Search in the Item Category name
        Q(item_brand__icontains=query) |  # Search in the Item brand
        Q(item_model__icontains=query) |  # Search in the Item model
        Q(item_frame_type_id__item_frame_type_name__icontains=query)  # Search in the Item Frame Type name
    )[:10]  # Limit the number of items returned

    results = [
        {
            'id': item.item_code,
            'text': f'{item.item_category_id} | {item.item_brand} | {item.item_model} | {item.item_frame_type_id}'
        }
        for item in items
    ]
    return JsonResponse({'items': results})

def item_price(request):
    item_id = request.GET.get('item_id')
    try:
        item = Item.objects.get(pk=item_id)
        return JsonResponse({'price': item.item_price})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
def sample_fucntion():
    pass
#_____________________________________SALES__________________________________________________________
def sales(request):
    return render(request, 'clinic/Sales/sales.html')