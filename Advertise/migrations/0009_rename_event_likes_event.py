# Generated by Django 5.1.4 on 2025-02-24 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Advertise', '0008_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='Event',
            new_name='event',
        ),
    ]
