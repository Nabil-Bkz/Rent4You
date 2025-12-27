from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContratLocationViewSet

router = DefaultRouter()
router.register(r'contrats', ContratLocationViewSet, basename='contrat')

urlpatterns = [
    path('', include(router.urls)),
]

