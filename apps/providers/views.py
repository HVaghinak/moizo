import coreapi
import coreschema
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from apps.providers.models import Provider, ProviderServiceArea
from apps.providers.serializers import ProviderSerializer, ProviderServiceAreaSerializer, FilterPolygonsSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all().prefetch_related(Prefetch('services'))
    serializer_class = ProviderSerializer
    http_method_names = ['post', 'patch', 'get', 'delete']


class ProviderServiceAreaViewSet(ModelViewSet):
    queryset = ProviderServiceArea.objects.all()
    serializer_class = ProviderServiceAreaSerializer
    http_method_names = ['post', 'patch', 'get', 'delete']


class FilterPolygonsAPIView(APIView):
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "latitude",
                required=True,
                schema=coreschema.Number(),
                description='Please provide latitude for filter'
            ),
            coreapi.Field(
                "longitude",
                required=True,
                schema=coreschema.Number(),
                description='Please provide longitude for filter'
            ),
        ]
    )
    serializer_class = FilterPolygonsSerializer

    def get(self, request):

        serializer = self.serializer_class(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        response = serializer.filter_polygons(serializer.validated_data)

        return Response(response, status=status.HTTP_200_OK)