# Generated by Django 5.0.3 on 2024-12-06 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0012_alter_copies_composer_alter_copies_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copies',
            name='composer',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='copies',
            name='name',
            field=models.TextField(),
        ),
    ]
