# Generated by Django 3.0.2 on 2020-01-27 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='account_created',
            field=models.DateField(auto_now_add=True, verbose_name='account created'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='account_updated',
            field=models.DateField(auto_now=True, verbose_name='account updated'),
        ),
    ]
