from django.db import models
from django.utils.timezone import now
# Create your models here.


class Item_Category(models.Model):
    item_category_id = models.AutoField(primary_key=True)
    item_category_name = models.CharField(max_length=50, null=True,blank=True)

    def __str__(self):
        return f"{self.item_category_name}"
    
class Item_Frame_Type(models.Model):
    frame_choices = [
        ('Plastic', 'Plastic'),
        ('Acetate','Acetate'),
        ('Metal','Metal'),
        ('Wood','Wood'),
        ('Titanium','Titanium'),

    ]
    item_frame_type_id = models.AutoField(primary_key=True)
    item_frame_type_name = models.CharField(max_length=20, choices=frame_choices)

    def __str__(self):
        return f"{self.item_frame_type_name}"

class Item(models.Model):
    item_code = models.AutoField(primary_key=True)
    item_brand = models.CharField(max_length=200)
    item_model = models.CharField(max_length=20,null=True,blank=True)
    item_price = models.FloatField()
    item_date_in = models.DateField(default=now)
    item_date_out = models.DateField(null=True,blank=True)
    item_quantity = models.IntegerField()
    item_color = models.CharField(max_length=100,null=True,blank=True)
    item_measurement = models.CharField(max_length=200,null=True,blank=True)
    item_category_id = models.ForeignKey(Item_Category, null=True, blank=True, on_delete=models.SET_NULL)
    item_frame_type_id = models.ForeignKey(Item_Frame_Type,on_delete=models.CASCADE, db_constraint=True, null=True , blank=True)

    def __str__(self):
        return f'{self.item_category_id} | {self.item_brand} | {self.item_model} | {self.item_frame_type_id}'

class Purchased_Item(models.Model):   
    pur_stat_choices = [
        ('Waiting', 'Waiting'), 
        ('For follow up', 'For follow up'), 
        ('Done', 'Done'),
    ]
    pur_id = models.AutoField(primary_key=True)
    pur_date_purchased = models.DateField(default=now)
    pur_stat = models.CharField(max_length=20, choices= pur_stat_choices)
    item_code =  models.ForeignKey(Item,null=True, blank=True, on_delete=models.SET_NULL)
    patient_id = models.ForeignKey('Patient', null=True, blank=True, on_delete=models.SET_NULL)
    payment_id = models.ForeignKey('Payment', null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.item_code},  {self.pur_date_purchased}"



class Payment(models.Model): 
    payment_method_choices = [
        ('Cash','Cash'),
        ('Debit Card', 'Debit Card'),
        ('Credit Card','Credit Card'),
        ('E Wallet','E Wallet'),
        ('Other','Other'),
    ]

    pay_terms_choices = [
        ('Installment', 'Installment'),
        ('Fully Paid', 'Fully Paid'),
    ]
    
    payment_id = models.AutoField(primary_key=True)
    payment_payed = models.FloatField(null=True,blank=True)
    payment_to_be_payed = models.FloatField(null=True,blank=True)
    payment_method = models.CharField(max_length=50,choices=payment_method_choices,default='Cash')
    payment_terms = models.CharField(max_length=20, choices=pay_terms_choices,default='Fully Paid')
    

    def __str__(self):
        return f" {self.payment_payed}, {self.payment_to_be_payed}"

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_fname = models.CharField(max_length=50)
    patient_lname = models.CharField(max_length=100)
    patient_initial = models.CharField(max_length=1, null=True, blank=True)
    patient_date_checked_up = models.DateField(default=now)
    patient_address = models.CharField(max_length=400)
    patient_occupation = models.CharField(max_length=500, null=True , blank=True)
    patient_birthdate = models.DateField()
    patient_contact = models.CharField(max_length=13)
    patient_diag = models.TextField(null=True,blank=True)
    pur_id = models.ForeignKey(Purchased_Item,null=True,blank=True,on_delete=models.SET_NULL)
    payment_id = models.ForeignKey(Payment,null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.patient_fname}, {self.patient_fname}, - Diagnosed with {self.patient_diag[:30]} ,{self.pur_id}, {self.payment_id}"
    
class Appointment(models.Model):
    app_status_choices = [
        ('Ongoing', 'Ongoing'),
        ('Waiting', 'Waiting'),
        ('Done', 'Done'),
    ]
    app_id = models.AutoField(primary_key=True)
    app_fname = models.CharField(max_length=50, null=True, blank=True)  # Temporarily allow nulls
    app_lname = models.CharField(max_length=50, null=True, blank=True)  # Temporarily allow nulls
    app_contact = models.CharField(max_length=11, null=True, blank=True)  # Temporarily allow nulls
    app_date = models.DateField()
    app_time = models.TimeField()
    app_status = models.CharField(max_length=50, choices=app_status_choices, default='Waiting')
    
