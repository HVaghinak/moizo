from rest_framework import serializers

from apps.providers.models import Provider, ProviderServiceArea


class ProviderServiceAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProviderServiceArea
        fields = '__all__'


class ProviderSerializer(serializers.ModelSerializer):
    services = ProviderServiceAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        fields = '__all__'


class FilterPolygonsSerializer(serializers.Serializer):

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    @staticmethod
    def filter_polygons(validated_data):

        lat_long_pair = [validated_data['latitude'], validated_data['longitude']]

        queryset = (
            ProviderServiceArea.objects
                               .select_related('provider')
                               .filter(polygon_coordinates__contains=lat_long_pair)
                               .values('name', 'provider__name', 'price')
        )

        return queryset
