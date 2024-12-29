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
        ('Platic', 'Plastic'),
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
    item_quantity = models.IntegerField()
    item_color = models.CharField(max_length=100,null=True,blank=True)
    item_measurement = models.CharField(max_length=200,null=True,blank=True)
    item_category_id = models.ForeignKey(Item_Category,on_delete=models.CASCADE, db_constraint=True)
    item_frame_type_id = models.ForeignKey(Item_Frame_Type,on_delete=models.CASCADE, db_constraint=True, null=True , blank=True)

    def __str__(self):
        return f'{self.item_category_id}, {self.item_brand} , {self.item_frame_type_id}'
    
class Diagnosed(models.Model):
    diag_id = models.AutoField(primary_key=True)
    diag_descript = models.TextField()
    diag_date = models.DateField()

    def __str__(self):
        return f'{self.diag_descript}, {self.diag_date}'

class Purchased_Item_Status(models.Model):
    pur_stat_choices = [
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done'),
    ]
    purchase_item_status_id = models.AutoField(primary_key=True)
    purchase_item_status_name = models.CharField(max_length=20, choices= pur_stat_choices)

    def __str__(self):
        return f"{self.purchase_item_status_name}"

class Purchased_Item(models.Model):   
    pur_id = models.AutoField(primary_key=True)
    pur_quantity = models.IntegerField()
    pur_date_purchased = models.DateField(default=now)
    pur_total_price =  models.FloatField()
    item_code =  models.ForeignKey(Item,null=True, blank=True, on_delete=models.SET_NULL)
    purchase_item_status_id = models.ForeignKey(Purchased_Item_Status, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.item_code}, {self.pur_quantity}, {self.pur_total_price}, {self.pur_date_purchased}"

class Payment_Terms(models.Model):
    pay_stat_choices = [
        ('Installment', 'Installment'),
        ('Fully Paid', 'Fully Paid'),
    ]
    pay_stat_id = models.AutoField(primary_key=True)
    pay_stat_name =models.CharField(max_length=20, choices=pay_stat_choices)

    def __str__(self):
        return f"{self.pay_stat_name}"

class Mode_of_Payment(models.Model):
    mop_choices = [
        ('Cash','Cash'),
        ('Debit Card', 'Debit Card'),
        ('Credit Card','Credit Card'),
        ('E Wallet','E Wallet'),
    ]
    mop_id = models.AutoField(primary_key=True)
    mop_name = models.CharField(max_length=50, choices=mop_choices)

    def __str__(self):
        return f"{self.mop_name}"
    
class Payment_Duration(models.Model):
    payment_duration_choices = [
        ('3 Months', '3 Months'),
        ('6 Months', '6 Months'),
        ('9 Months', '9 Months'),
        ('12 Months', '12 Months'),
    ]
    payment_duration_id = models.AutoField(primary_key=True)
    payment_duration_name = models.CharField(max_length=50,choices=payment_duration_choices)
    payment_duration_start = models.DateField(default=now)
    payment_duration_end =  models.DateField()
    
    def __str__(self):
        return f"{self.payment_duration_name},{self.payment_duration_choices},{self.payment_duration_start}, {self.payment_duration_end} "

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_payed = models.FloatField()
    payment_to_be_payed = models.FloatField(null=True,blank=True)
    pay_stat_id = models.ForeignKey(Payment_Terms, null=True, blank=True, on_delete=models.SET_NULL)
    mop_id = models.ForeignKey(Mode_of_Payment, null=True, blank=True, on_delete=models.SET_NULL)
    payment_duration_id = models.ForeignKey(Payment_Duration, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.mop_id}, {self.pay_stat_id}, {self.payment_payed}, {self.payment_to_be_payed}, {self.payment_duration_id}"

class Patient(models.Model):

    patient_id = models.AutoField(primary_key=True)
    patient_fname = models.CharField(max_length=50)
    patient_lname = models.CharField(max_length=100)
    patient_initial = models.CharField(max_length=1, null=True, blank=True)
    patient_address = models.CharField(max_length=400)
    patient_occupation = models.CharField(max_length=500, null=True , blank=True)
    patient_birthdate = models.DateField()
    patient_contact = models.CharField(max_length=13)
    diag_id = models.ForeignKey(Diagnosed, null=True,blank=True,on_delete=models.CASCADE)
    pur_id = models.ForeignKey(Purchased_Item,null=True,blank=True,on_delete=models.SET_NULL)
    payment_id = models.ForeignKey(Payment,null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.pur_id}, {self.payment_id}, {self.patient_fname}, {self.patient_lname}, {self.diag_id}"
    
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
    
