# Generated by Django 5.0.3 on 2024-12-05 13:47

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0010_alter_copies_part'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('requested_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]