from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReclamationViewSet, RapportViewSet, EtatVehiculeViewSet

router = DefaultRouter()
router.register(r'reclamations', ReclamationViewSet, basename='reclamation')
router.register(r'rapports', RapportViewSet, basename='rapport')
router.register(r'etats-vehicules', EtatVehiculeViewSet, basename='etat-vehicule')

urlpatterns = [
    path('', include(router.urls)),
]

