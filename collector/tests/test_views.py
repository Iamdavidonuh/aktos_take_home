import uuid

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from collector import models


class TestBase(APITestCase):
    """Contains helper functions"""

    @staticmethod
    def create_customer_balance(
        name: str, ssn: str, balance: float
    ) -> models.ConsumerBalance:
        """creates a simple customer balance object

        Args:
            name (str): Name of customer
            ssn (str): social security number
            balance (float): amount of money

        Returns:
            models.ConsumerBalance: customer balance object
        """
        customer = models.ConsumerBalance.objects.create(
            client_ref_no=uuid.uuid4(),
            balance=balance,
            status=models.ConsumerBalanceChoices.IN_COLLECTION,
            consumer_name=name,
            ssn=ssn,
            consumer_address="123 Test Address",
        )
        return customer

    def create_multiple_customer_balance(self, max_number):
        """Creates n-1 amount of ConsumerBalance objects

        Args:
            max_number (int): total amount of objects to create
        """
        for idx in range(1, max_number):
            consumer_name = f"Test User{idx}"
            balance = 100.00 * idx
            ssn = f"123-4223-82{idx}"
            _ = self.create_customer_balance(
                name=consumer_name, balance=balance, ssn=ssn
            )


class TestConsumerViewsets(TestBase):
    def setUp(self) -> None:
        super().setUp()

        self.create_multiple_customer_balance(5)

    def test_get_consumers_success(self):
        get_consumers_endpoint = reverse("collector:consumers-list")
        response = self.client.get(get_consumers_endpoint)
        consumers = models.ConsumerBalance.objects.all()
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(len(response.json()["results"]) == consumers.count())

    def test_get_consumers_query_by_min_max_balances(self):
        expected_response_length = 3
        query_endpoint = (
            f'{reverse("collector:consumers-list")}?min_balance=100&max_balance=300'
        )
        response = self.client.get(query_endpoint)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(len(response.json()["results"]) == expected_response_length)

    def test_get_consumers_query_by_consumer_name_uses_icontains_lookup(self):
        query_endpoint = f'{reverse("collector:consumers-list")}?consumer_name=test'
        response = self.client.get(query_endpoint)
        consumers = models.ConsumerBalance.objects.all()
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(len(response.json()["results"]) == consumers.count())

    def test_get_consumers_query_by_status_works(self):
        query_endpoint = f'{reverse("collector:consumers-list")}?status=in_collection'
        response = self.client.get(query_endpoint)
        consumers = models.ConsumerBalance.objects.all()
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(len(response.json()["results"]) == consumers.count())


class TestCSVUPloadView(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_fixtures_path = settings.BASE_DIR / "collector" / "fixtures" / "test"

    def test_csv_upload_succeeds(self):
        upload_csv_url = reverse("collector:upload-consumers-list")

        upload_success_msg = "Records created successfully"

        test_csv_path = self.test_fixtures_path / "test_balances.csv"

        with open(test_csv_path, "rb") as csv_file:
            uploaded_file = SimpleUploadedFile(
                csv_file.name, csv_file.read(), content_type="text/csv"
            )
            response = self.client.post(
                upload_csv_url, {"file": uploaded_file}, format="multipart"
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], upload_success_msg)

        # count db items, should be total csv items(3)
        self.assertTrue(models.ConsumerBalance.objects.count(), 3)
