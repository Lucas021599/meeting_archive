from rest_framework import status, views
from rest_framework.response import Response


class HealthCheckView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(status.HTTP_200_OK)
