"""
URLs for statistics app
"""
from django.urls import path
from .views import StatisticsView, ExportStatisticsView

urlpatterns = [
    path('', StatisticsView.as_view(), name='statistics'),
    path('export/', ExportStatisticsView.as_view(), name='export-statistics'),
]

