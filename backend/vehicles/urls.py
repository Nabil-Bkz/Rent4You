from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculeViewSet, DepotViewSet

router = DefaultRouter()
router.register(r'vehicules', VehiculeViewSet, basename='vehicule')
router.register(r'depots', DepotViewSet, basename='depot')

urlpatterns = [
    path('', include(router.urls)),
]

