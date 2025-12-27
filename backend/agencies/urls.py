from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgenceViewSet, DemandePartenariatViewSet, DemandeCompteAdminViewSet

router = DefaultRouter()
router.register(r'agences', AgenceViewSet, basename='agence')
router.register(r'partenariats', DemandePartenariatViewSet, basename='partenariat')
router.register(r'comptes-admin', DemandeCompteAdminViewSet, basename='compte-admin')

urlpatterns = [
    path('', include(router.urls)),
]

