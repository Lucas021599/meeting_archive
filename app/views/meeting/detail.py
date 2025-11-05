from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.generics import RetrieveAPIView

from app.exceptions.exception import NotFoundException
from app.models.meeting import Meeting
from app.serializers.error import ErrorSerializer
from app.serializers.meeting import MeetingSerializer


class MeetingDetailView(RetrieveAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

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
