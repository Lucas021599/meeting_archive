import uuid

from drf_spectacular.utils import OpenApiResponse, extend_schema
from qdrant_client.models import PointStruct
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers.vector import VectorInsertRequestSerializer
from app.utils import embed_text
from meeting_archive.qdrant import get_qdrant_client
from meeting_archive.settings import COLLECTION_NAME


class InsertView(APIView):
    @extend_schema(
        summary="Insert Points",
        description="Store a sentence in the vector database",
        request=VectorInsertRequestSerializer,
        responses={
            201: OpenApiResponse(description="Text inserted successfully"),
        },
        tags=["Vector"],
    )
    def post(self, request):
        text = request.data.get("text")
        if not text:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"error": "Text is required"}
            )
        embedding = embed_text(text)
        client = get_qdrant_client()
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()), vector=embedding, payload={"text": text}
                )
            ],
        )
        return Response(
            data={"message": "Text inserted successfully"},
            status=status.HTTP_201_CREATED,
        )
