from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    code = serializers.CharField(help_text="에러 코드")
    message = serializers.CharField(help_text="에러 메세지")
    status_code = serializers.IntegerField(help_text="HTTP 상태 코드")
