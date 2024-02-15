from rest_framework import mixins, viewsets

from collector import models, serializers


class ConsumersViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.CustomerBalance.objects.all()
    serializer_class = serializers.ConsumerBalanceSerializer
