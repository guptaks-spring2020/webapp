from decimal import Decimal
import uuid
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class BillFile(models.Model):
    file_name = models.CharField(max_length=50, null=False, blank=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.FileField(blank=False, null=False)
    upload_date = models.DateTimeField(verbose_name='account created', auto_now_add=True)


class Bills(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='owner_id')
    created_ts = models.DateTimeField(verbose_name='account created', auto_now_add=True)
    updated_ts = models.DateTimeField(verbose_name='account updated', auto_now=True)
    vendor = models.CharField(max_length=50, null=False, blank=False)
    bill_date = models.DateField(verbose_name='bill date')
    due_date = models.DateField(verbose_name='due date')
    amount_due = models.DecimalField(
                                        verbose_name='amount due',
                                        max_digits=20,
                                        decimal_places=2,
                                        validators=[MinValueValidator(Decimal('0.01'))]
                                    )

    payment_status = (
        ('paid', 'paid'),
        ('due', 'due'),
        ('past_due', 'past_due'),
        ('no_payment_required', 'no_payment_required'),
    )

    paymentStatus = models.CharField(
        max_length=20,
        choices=payment_status
    )
    categories = ArrayField(
            models.CharField(max_length=20, blank=False),
            size=8,
        )

    attachment = models.ForeignKey(BillFile, on_delete=models.CASCADE, null=True)
