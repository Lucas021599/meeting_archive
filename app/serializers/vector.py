from rest_framework import serializers


class VectorInsertRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
