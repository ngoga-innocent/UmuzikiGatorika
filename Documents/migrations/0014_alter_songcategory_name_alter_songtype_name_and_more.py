# Generated by Django 5.0.3 on 2024-12-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0013_alter_copies_composer_alter_copies_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songcategory',
            name='name',
            field=models.CharField(default='Others', max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='songtype',
            name='name',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='songtype',
            name='season',
            field=models.CharField(default='Ibihe Bisanzwe', max_length=512, null=True),
        ),
        migrations.AlterModelTable(
            name='copies',
            table='copies',
        ),
    ]