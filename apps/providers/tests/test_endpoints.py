import json
import random

from faker import Faker
from rest_framework.test import APITestCase


class TestEndpoints(APITestCase):

    def setUp(self):

        self.faker = Faker()
        self.provider_url = '/providers/'
        self.service_url = '/providers-service-area/'
        self.filter_url = '/provider/filter-polygons/'
        self.provider_validated_data = {
            "name": self.faker.company(),
            "email": self.faker.company_email(),
            "currency": '77',
            "language": self.faker.language_code(),
            "phone_number": self.faker.phone_number()
        }
        self.service_validated_data = {
            "name": self.faker.name(),
            "price": self.faker.pyfloat(),
            "polygon_coordinates": [
                [float(self.faker.latitude()), float(self.faker.longitude())] for _ in range(random.randint(1, 10))
            ]
        }

    def test_endpoints(self):

        provider, service = self._create_mock_data()

        provider_created = provider.status_code == 201

        service_created = service.status_code == 201

        provider_new_name = self.faker.company()
        provider_object_url = '{}{}/'.format(self.provider_url, provider.data['id'])
        patched_provider = self.client.patch(provider_object_url, data={'name': provider_new_name})

        provider_updated = patched_provider.data['name'] == provider_new_name

        service_new_name = self.faker.name()
        service_object_url = '{}{}/'.format(self.service_url, service.data['id'])
        patched_service = self.client.patch(service_object_url, data={'name': service_new_name})

        service_updated = patched_service.data['name'] == service_new_name

        service_deleted = self.client.delete(service_object_url).status_code == 200
        provider_deleted = self.client.delete(provider_object_url).status_code == 200

        conditions = all([
            provider_created,
            service_created,
            provider_updated,
            service_updated,
            service_deleted,
            provider_deleted,
        ])

        self.assertTrue(True, conditions)

    def test_filter(self):
        filtered_cords = [float(self.faker.latitude()), float(self.faker.longitude())]

        provider, service = self._create_mock_data(filtered_item=filtered_cords)

        query_params = {
            'latitude': filtered_cords[0],
            'longitude': filtered_cords[1]
        }

        expected_dict = {
            'provider__name': provider.data['name'],
            'price': service.data['price'],
            'name': service.data['name']
        }

        response = self.client.get(self.filter_url, data=query_params)

        self.assertDictEqual(response.data[0], expected_dict)

    def _create_mock_data(self, filtered_item=None):

        if filtered_item:
            self.service_validated_data['polygon_coordinates'].append(filtered_item)

        provider = self.client.post(self.provider_url, data=self.provider_validated_data)

        self.service_validated_data["provider"] = provider.data['id']

        self.service_validated_data = json.dumps(self.service_validated_data)
        service = self.client.post(self.service_url, data=self.service_validated_data, content_type='application/json')

        return provider, service
