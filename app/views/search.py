from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers.vector import VectorSearchResponseSerializer
from app.utils import embed_text
from meeting_archive.qdrant import get_qdrant_client
from meeting_archive.settings import COLLECTION_NAME


class SearchView(APIView):
    @extend_schema(
        summary="Query Points",
        description="Search for similar sentences in the vector database",
        parameters=[
            OpenApiParameter(
                name="query",
                description="The query to search for",
                required=True,
                type=str,
            ),
        ],
        responses={
            200: VectorSearchResponseSerializer(many=True),
        },
        tags=["Vector"],
    )
    def get(self, request):
        query = request.query_params.get("query")
        if not query:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"error": "Query is required"}
            )
        client = get_qdrant_client()
        result = client.query_points(
            collection_name=COLLECTION_NAME, query=embed_text(query), limit=2
        )
        serializer = VectorSearchResponseSerializer(
            [
                {
                    "id": str(p.id),
                    "score": p.score,
                    "text": p.payload.get("text") if p.payload else None,
                }
                for p in result.points
            ],
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
