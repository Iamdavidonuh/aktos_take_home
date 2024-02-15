from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from collector import models


class TestConsumerViewsets(APITestCase):
    def test_get_consumers_success(self):
        get_consumers_endpoint = reverse("collector:consumers-list")
        response = self.client.get(get_consumers_endpoint)
        consumers = models.CustomerBalance.objects.all()
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(len(response.json()) == consumers.count())
