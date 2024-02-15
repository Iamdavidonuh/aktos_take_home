from django_filters import rest_framework as djrf_filters
from rest_framework import viewsets

from collector import filter_backend, models, serializers


class ConsumersViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.CustomerBalance.objects.all()
    serializer_class = serializers.ConsumerBalanceSerializer

    filter_backends = [djrf_filters.DjangoFilterBackend]
    filterset_class = filter_backend.ConsumerBalanceFilter
