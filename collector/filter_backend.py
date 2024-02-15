from django_filters import rest_framework as filters

from collector import models


class ConsumerBalanceFilter(filters.FilterSet):
    consumer_name = filters.CharFilter(lookup_expr="icontains")
    min_balance = filters.NumberFilter(field_name="balance", lookup_expr="gte")
    max_balance = filters.NumberFilter(field_name="balance", lookup_expr="lte")

    class Meta:
        model = models.CustomerBalance
        fields = ["status"]
