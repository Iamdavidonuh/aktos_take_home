import pandas as pd
from django.conf import settings

from collector import models


class BadHeadersException(Exception):
    pass


def verify_headers(headers: list) -> bool:
    return bool(set(settings.EXPECTED_CSV_HEADERS) == set(headers))


def save_consumer_balance_from_csv(csv_file_or_path):
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

    if not verify_headers(df.columns.tolist()):
        raise BadHeadersException(
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

        if not models.ConsumerBalance.objects.filter(
            client_ref_no=client_ref_no
        ).exists():
            # customer_object_list.append(
            models.ConsumerBalance(
                client_ref_no=client_ref_no,
                status=status,
                consumer_name=consumer_name,
                consumer_address=consumer_address,
                ssn=ssn,
                balance=balance,
            ).save()
        # )
    return models.ConsumerBalance.objects.bulk_create(customer_object_list)
