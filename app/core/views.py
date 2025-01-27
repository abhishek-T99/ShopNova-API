from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema


@extend_schema(request=None, responses={200: {"healthy": "boolean"}})
class HealthCheckView(GenericAPIView):
    """
    Health check endpoint to verify that the service is running.
    """

    def get(self, request):
        """
        Health check endpoint to verify that the service is running.
        """
        return Response({"healthy": True}, status=status.HTTP_200_OK)
