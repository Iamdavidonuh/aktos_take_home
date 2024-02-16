import uuid
import pandas as pd
from django.conf import settings
from django.db.models import QuerySet

from collector import models


class BadHeadersException(Exception):
    pass


class CSVConsumerHandler:

    @staticmethod
    def verify_headers(headers: list) -> bool:
        return bool(set(settings.EXPECTED_CSV_HEADERS) == set(headers))

    @staticmethod
    def is_duplicate_record(query: QuerySet, row: pd.Series) -> bool:
        """Confirms a record to be stored is a duplicate record after the client_ref_no exists"""
        status = str(row["status"]).lower()
        consumer_name = row["consumer name"]
        consumer_address = " ".join(str(row["consumer address"]).split())

        ssn = row["ssn"]
        balance = row["balance"]

        # All short-circuits, meaning, if any condition fails it returns a False without processing the rest,
        # Meaning the last check shouldn't return a Nonetype Error
        return all(
            [
                (
                    query.filter(status=status)
                    .filter(consumer_name=consumer_name)
                    .filter(ssn=ssn)
                    .filter(balance=balance)
                ).exists(),
                query.exists(),
                query.count() == 1,
                query.first().consumer_address.split() == consumer_address.split(),
            ]
        )

    def save_consumer_balance_from_csv(self, csv_file_or_path):
        """
        Helper to create consumer_balance records from csv file

        Args:
            csv_file_or_path (byte or str): file path or bytes

        Raises:
            BadHeadersException: Incorrect csv headers

        Returns:
            List[models.ConsumerBalance]: List of created ConsumerBalance objects

        """

        df = pd.read_csv(csv_file_or_path)
        # Convert column names to lowercase
        df.columns = df.columns.str.lower()

        if not self.verify_headers(df.columns.tolist()):
            raise BadHeadersException(
                f"Bad Header Format, CSV should have the following in no order: {settings.EXPECTED_CSV_HEADERS}"
            )

        for _, row in df.iterrows():
            client_ref_no = row["client reference no"]

            query = models.ConsumerBalance.objects.filter(client_ref_no=client_ref_no)

            if query.exists():
                if self.is_duplicate_record(query, row):
                    continue
                else:
                    # only client ref number needs changing

                    client_ref_no = uuid.uuid4()

            models.ConsumerBalance(
                client_ref_no=client_ref_no,
                status=str(row["status"]).lower(),
                consumer_name=row["consumer name"],
                consumer_address=row["consumer address"],
                ssn=row["ssn"],
                balance=row["balance"],
            ).save()
