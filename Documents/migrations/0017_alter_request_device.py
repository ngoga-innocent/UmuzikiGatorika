# Generated by Django 5.0.3 on 2024-12-07 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0016_request_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='device',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]