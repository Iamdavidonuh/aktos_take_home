from io import StringIO
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from collector import models


class TestLoadConsumers(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_fixtures_path = settings.BASE_DIR / "collector" / "fixtures" / "test"

    def test_command_output(self):
        out = StringIO()
        call_command(
            "load_consumers",
            "--path",
            f"{self.test_fixtures_path}/test_balances.csv",
            stdout=out,
        )
        self.assertIn("Successfully Saved Data", out.getvalue())

    def test_call_command_loads_data(self):

        call_command(
            "load_consumers", "--path", f"{self.test_fixtures_path}/test_balances.csv"
        )
        self.assertEqual(models.ConsumerBalance.objects.count(), 3)

    def test_call_command_loads_no_duplicate_data(self):

        # populate database
        call_command(
            "loaddata", f"{self.test_fixtures_path}/test_consumer.json", verbosity=0
        )

        call_command(
            "load_consumers", "--path", f"{self.test_fixtures_path}/test_balances.csv"
        )
        # DB count remains 3 instead of 6
        self.assertEqual(models.ConsumerBalance.objects.count(), 3)
