from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from app.exceptions.exception import NotFoundException
from app.models.meeting import Meeting
from app.serializers.error import ErrorSerializer
from app.serializers.meeting import MeetingSerializer
from app.utils import qdrant_delete, qdrant_update_payload, qdrant_upsert


class MeetingDetailView(RetrieveUpdateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    http_method_names = ["get", "patch"]

    @extend_schema(
        summary="get_meeting",
        description="Get a meeting by id",
        responses={
            200: MeetingSerializer,
            404: OpenApiResponse(
                response=ErrorSerializer,
                examples=[
                    NotFoundException.example(),
                ],
            ),
        },
        tags=["Meeting"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if (
            "summary" in validated_data
            and validated_data["summary"] != instance.summary
        ):
            qdrant_delete(instance.id)
            qdrant_upsert(
                {
                    "text": validated_data["summary"],
                    "meeting_id": instance.id,
                    "category": instance.category,
                }
            )
        else:
            if (
                "category" in validated_data
                and validated_data["category"] != instance.category
            ):
                qdrant_update_payload(
                    instance.id, {"category": validated_data["category"]}
                )
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="update_meeting",
        description="Update a meeting by id",
        responses={
            200: MeetingSerializer,
            404: OpenApiResponse(
                response=ErrorSerializer,
                examples=[
                    NotFoundException.example(),
                ],
            ),
        },
        tags=["Meeting"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
