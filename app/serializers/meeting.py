import uuid

from qdrant_client.models import PointStruct
from rest_framework import serializers

from app.models.meeting import Meeting
from app.utils import embed_text
from meeting_archive.qdrant import get_qdrant_client
from meeting_archive.settings import COLLECTION_NAME


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"

    def create(self, validated_data):
        meeting = super().create(validated_data)
        # TODO: 현재는 전체 내용을 임베딩 변환, 추후 내용을 의미단위로 자르는 로직 추가 필요
        embedding = embed_text(meeting.summary)
        client = get_qdrant_client()
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={"text": meeting.summary, "meeting_id": meeting.id},
                )
            ],
        )
        return meeting
