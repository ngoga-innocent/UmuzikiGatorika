# Generated by Django 5.0.3 on 2024-12-07 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0015_alter_copies_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='device',
            field=models.CharField(default='sasasasasasasasa', max_length=255),
            preserve_default=False,
        ),
    ]