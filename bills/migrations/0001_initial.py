# Generated by Django 3.0.2 on 2020-01-27 04:43

from decimal import Decimal
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_ts', models.DateTimeField(auto_now_add=True, verbose_name='account created')),
                ('updated_ts', models.DateTimeField(auto_now=True, verbose_name='account updated')),
                ('vendor', models.CharField(max_length=50)),
                ('bill_date', models.DateField(verbose_name='bill date')),
                ('due_date', models.DateField(verbose_name='due date')),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='amount due')),
                ('paymentStatus', models.CharField(choices=[('paid', 'Freshman'), ('due', 'Sophomore'), ('past_due', 'past_due'), ('no_payment_required', 'no_payment_required')], max_length=20)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=8)),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner_id')),
            ],
        ),
    ]
