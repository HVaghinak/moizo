from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Provider(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ProviderServiceArea(models.Model):

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    price = models.FloatField()
    polygon_coordinates = ArrayField(base_field=ArrayField(base_field=models.FloatField(), size=2))
