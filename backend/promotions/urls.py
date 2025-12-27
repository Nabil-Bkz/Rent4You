from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CodePromoViewSet

router = DefaultRouter()
router.register(r'codes-promo', CodePromoViewSet, basename='code-promo')

urlpatterns = [
    path('', include(router.urls)),
]

