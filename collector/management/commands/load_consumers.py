from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from collector import models
import os
import pandas as pd


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

        df = pd.read_csv(csv_path)
        # Convert column names to lowercase
        df.columns = df.columns.str.lower()

        if not self.verify_headers(df.columns.tolist()):
            raise CommandError(
                f"Bad Header Format, CSV should have the following in no order: {settings.EXPECTED_CSV_HEADERS}"
            )

        customer_object_list = []

        for _, row in df.iterrows():
            client_ref_no = row["client reference no"]
            status = str(row["status"]).lower()
            consumer_name = row["consumer name"]
            consumer_address = row["consumer address"]
            ssn = row["ssn"]
            balance = row["balance"]

            if not models.CustomerBalance.objects.filter(
                client_ref_no=client_ref_no
            ).exists():
                # customer_object_list.append(
                models.CustomerBalance(
                    client_ref_no=client_ref_no,
                    status=status,
                    consumer_name=consumer_name,
                    consumer_address=consumer_address,
                    ssn=ssn,
                    balance=balance,
                ).save()
            # )
        models.CustomerBalance.objects.bulk_create(customer_object_list)
        self.stdout.write(self.style.SUCCESS("Successfully Saved Data from csv file"))
