from django_filters import rest_framework as djrf_filters
from rest_framework import mixins, response, status, viewsets

from collector import filter_backend, models, serializers


class ConsumersViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.ConsumerBalance.objects.all()
    serializer_class = serializers.ConsumerBalanceSerializer

    filter_backends = [djrf_filters.DjangoFilterBackend]
    filterset_class = filter_backend.ConsumerBalanceFilter


class ConsumerBalanceCSVUploadViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = models.ConsumerBalance.objects.all()
    serializer_class = serializers.ConsumerCSVUploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            {"message": "Records created successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
