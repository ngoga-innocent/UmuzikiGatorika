# Generated by Django 5.0.3 on 2024-11-30 08:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advertise', '0004_remove_trendingsongs_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='trendingsongs',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
