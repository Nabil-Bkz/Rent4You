"""
Rent4You URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/agencies/', include('agencies.urls')),
    path('api/vehicles/', include('vehicles.urls')),
    path('api/reservations/', include('reservations.urls')),
    path('api/contracts/', include('contracts.urls')),
    path('api/complaints/', include('complaints.urls')),
    path('api/partnerships/', include('partnerships.urls')),
    path('api/promotions/', include('promotions.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/statistics/', include('statistics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
