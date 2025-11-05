from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from app.views.health import HealthCheckView
from app.views.insert import InsertView
from app.views.meeting.detail import MeetingDetailView
from app.views.meeting.list_create import MeetingListCreateView
from app.views.search import SearchView

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(), name="redoc"),
    path("health/", HealthCheckView.as_view(), name="health"),
    path("api/insert/", InsertView.as_view(), name="insert"),
    path("api/search/", SearchView.as_view(), name="search"),
    path("api/meeting/", MeetingListCreateView.as_view(), name="meeting-create"),
    path("api/meeting/<int:id>/", MeetingDetailView.as_view(), name="meeting-detail"),
]
