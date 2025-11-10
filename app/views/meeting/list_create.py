from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from app.models.meeting import Meeting
from app.serializers.meeting import MeetingListRequestSerializer, MeetingSerializer
from app.utils import calculate_points_score, query_points


class MeetingListCreateView(ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def get_queryset(self):
        serializer = MeetingListRequestSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if not data["query"]:
            self.queryset = (
                self.queryset.filter(category=data["category"])
                if data["category"]
                else self.queryset
            )
            return self.queryset.order_by("-id")

        result = query_points(data["category"], data["query"])
        meeting_ids = calculate_points_score(result.points)
        queryset = self.queryset.filter(id__in=meeting_ids)
        return sorted(queryset, key=lambda x: meeting_ids.index(x.id))

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

    @extend_schema(
        summary="get_meetings",
        description="Get meetings by query",
        parameters=MeetingListRequestSerializer,
        responses={
            200: MeetingSerializer(many=True),
        },
        tags=["Meeting"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
