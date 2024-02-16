from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class ConsumerBalanceChoices(models.TextChoices):
    INACTIVE = "inactive", _("INACTIVE")
    PAID_IN_FULL = "paid_in_full", _("PAID IN FULL")
    IN_COLLECTION = "in_collection", _("IN COLLECTION")


class ConsumerBalance(models.Model):
    client_ref_no = models.UUIDField(
        verbose_name="Client reference number", unique=True
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=25,
        default=ConsumerBalanceChoices.INACTIVE,
        choices=ConsumerBalanceChoices.choices,
    )
    consumer_name = models.CharField(max_length=100)
    consumer_address = models.TextField()
    ssn = models.CharField(max_length=20)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Consumer Balance"
        verbose_name_plural = "Consumer Balances"

    def __str__(self) -> str:
        return f"Consumer Balance for {self.consumer_name}"
