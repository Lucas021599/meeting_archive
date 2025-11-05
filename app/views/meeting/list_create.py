from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from app.models.meeting import Meeting
from app.serializers.meeting import MeetingSerializer


class MeetingListCreateView(ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    @extend_schema(
        summary="create_meeting",
        description="Create a meeting in rdb, qdrant",
        request=MeetingSerializer,
        responses={
            201: MeetingSerializer,
        },
        tags=["Meeting"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
