import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from collector import utils


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, required=True)

    @staticmethod
    def verify_headers(headers: list) -> bool:
        return bool(set(settings.EXPECTED_CSV_HEADERS) == set(headers))

    def handle(self, *args, **options):
        csv_path = options["path"]

        if not os.path.isfile(csv_path):
            raise CommandError(f"Invalid path: {csv_path} File does not exist")

        try:
            utils.save_consumer_balance_from_csv(csv_path)
        except utils.BadHeadersException as err:
            raise CommandError(f"Error Saving csv file: {err}")

        self.stdout.write(self.style.SUCCESS("Successfully Saved Data from csv file"))
