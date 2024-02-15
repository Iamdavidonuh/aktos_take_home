from django.test import TestCase
from collector import models
import uuid


# Create your tests here.


class TestCustomerBalanceModel(TestCase):

    def test_customer_balance_creation_succeeds(self):
        payload = dict(
            client_ref_no=uuid.uuid4(),
            balance=6000.08,
            consumer_name="David Test",
            consumer_address="123 oriental express",
            ssn="123-44433-12",
            status=models.CustomerBalanceChoices.IN_COLLECTION,
        )
        created = models.CustomerBalance.objects.create(**payload)

        db_data = models.CustomerBalance.objects.first()
        self.assertEqual(created, db_data)

    def test_customer_balance_default_value_for_status(self):

        payload = dict(
            client_ref_no=uuid.uuid4(),
            balance=6000.08,
            consumer_name="David Test",
            consumer_address="123 oriental express",
            ssn="123-44433-12",
        )
        models.CustomerBalance.objects.create(**payload)

        db_data = models.CustomerBalance.objects.first()

        self.assertTrue(db_data.status, models.CustomerBalanceChoices.INACTIVE)
