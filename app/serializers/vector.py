from rest_framework import serializers


class VectorInsertRequestSerializer(serializers.Serializer):
    text = serializers.CharField()


class VectorSearchResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    score = serializers.FloatField()
    text = serializers.CharField()
