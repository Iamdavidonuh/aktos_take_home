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
        csv_data = TextIOWrapper(validated_data["file"], encoding="utf-8")
        csv_hander = utils.CSVConsumerHandler()
        csv_hander.save_consumer_balance_from_csv(csv_file_or_path=csv_data)
        return True

    def to_representation(self, instance):
        return {}
