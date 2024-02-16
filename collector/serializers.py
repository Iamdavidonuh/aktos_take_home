from io import TextIOWrapper

import pandas as pd
from rest_framework import serializers

from collector import models, utils


class ConsumerBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConsumerBalance
        fields = "__all__"


class ConsumerCSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        csv_file = validated_data["file"]
        csv_data = TextIOWrapper(csv_file, encoding="utf-8")
        objs = utils.save_consumer_balance_from_csv(csv_file_or_path=csv_data)
        return objs

    def to_representation(self, instance):
        return {}
