# Generated by Django 3.0.2 on 2020-02-11 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0003_auto_20200210_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billfile',
            name='file_name',
            field=models.CharField(max_length=100),
        ),
    ]
