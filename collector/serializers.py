from rest_framework import serializers

from collector import models


class ConsumerBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConsumerBalance
        fields = "__all__"
