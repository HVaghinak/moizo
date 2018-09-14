from django.urls import path
from . import views

urlpatterns = [
    path('filter-polygons/', views.FilterPolygonsAPIView.as_view()),
]