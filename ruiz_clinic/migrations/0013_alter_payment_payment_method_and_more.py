# Generated by Django 5.1.4 on 2024-12-19 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0012_remove_payment_pay_stat_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Debit Card', 'Debit Card'), ('Credit Card', 'Credit Card'), ('E Wallet', 'E Wallet'), ('Other', 'Other')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_terms',
            field=models.CharField(choices=[('Installment', 'Installment'), ('Fully Paid', 'Fully Paid')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]