from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomerBalanceChoices(models.TextChoices):

    INACTIVE = "INACTIVE", _("INACTIVE")
    PAID_IN_FULL = "PAID_IN_FULL", _("PAID IN FULL")
    IN_COLLECTION = "IN_COLLECTION", _("IN COLLECTION")


class CustomerBalance(models.Model):

    client_ref_no = models.UUIDField(
        verbose_name="Client reference number", unique=True
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=25,
        default=CustomerBalanceChoices.INACTIVE,
        choices=CustomerBalanceChoices.choices,
    )
    consumer_name = models.CharField(max_length=100)
    consumer_address = models.TextField()
    ssn = models.CharField(max_length=20)

    class Meta:

        verbose_name = "Customer Balance"
        verbose_name_plural = "Customer Balances"
