from rest_framework import serializers

from app.models.meeting import Meeting
from app.utils import qdrant_upsert


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"

    def create(self, validated_data):
        meeting = super().create(validated_data)
        # TODO: 현재는 전체 내용을 임베딩 변환, 추후 내용을 의미단위로 자르는 로직 추가 필요
        qdrant_upsert(
            {
                "text": meeting.summary,
                "meeting_id": meeting.id,
                "category": meeting.category,
            }
        )
        return meeting


class MeetingListRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    count = serializers.IntegerField(required=False, default=10)
    query = serializers.CharField(required=False, default=None)
    category = serializers.CharField(required=False, default=None)
