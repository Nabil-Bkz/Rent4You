from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, LoginView, ProfileView, LocataireViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'locataires', LocataireViewSet, basename='locataire')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

