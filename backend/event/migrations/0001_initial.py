# Generated by Django 3.2.9 on 2021-12-02 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

import event.helpers
import event.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=5000)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('max_occupancy', models.IntegerField()),
                ('current_occupancy', models.IntegerField(default=0)),
                ('location', models.CharField(max_length=50)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_completed', models.BooleanField(default=False)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('payment_deadline', models.DateTimeField(default=event.helpers.user_event_deadline)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='event.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
