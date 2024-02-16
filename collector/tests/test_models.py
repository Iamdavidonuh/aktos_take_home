import uuid

from django.test import TestCase

from collector import models

# Create your tests here.


class TestConsumerBalanceModel(TestCase):
    def test_customer_balance_creation_succeeds(self):
        payload = {
            "client_ref_no": uuid.uuid4(),
            "balance": 6000.08,
            "consumer_name": "David Test",
            "consumer_address": "123 oriental express",
            "ssn": "123-44433-12",
            "status": models.ConsumerBalanceChoices.IN_COLLECTION,
        }

        created = models.ConsumerBalance.objects.create(**payload)

        db_data = models.ConsumerBalance.objects.first()
        self.assertEqual(created, db_data)

    def test_customer_balance_default_value_for_status(self):
        payload = {
            "client_ref_no": uuid.uuid4(),
            "balance": 6000.08,
            "consumer_name": "David Test",
            "consumer_address": "123 oriental express",
            "ssn": "123-44433-12",
        }
        models.ConsumerBalance.objects.create(**payload)

        db_data = models.ConsumerBalance.objects.first()

        self.assertTrue(db_data.status, models.ConsumerBalanceChoices.INACTIVE)
