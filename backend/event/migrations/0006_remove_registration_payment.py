# Generated by Django 3.2.9 on 2022-01-19 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_registration_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='payment',
        ),
    ]
