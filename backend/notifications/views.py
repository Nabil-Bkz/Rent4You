"""
Views for notifications
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.notifications import Notification, NotificationService
from .serializers import NotificationSerializer, NotificationMarkReadSerializer
from core.response import APIResponse


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get notifications for current user"""
        queryset = Notification.objects.filter(user=self.request.user)
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return APIResponse.success(
            data=NotificationSerializer(notification).data,
            message="Notification marquée comme lue."
        )
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        serializer = NotificationMarkReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data.get('mark_all'):
            count = NotificationService.mark_all_as_read(request.user)
            return APIResponse.success(
                message=f"{count} notification(s) marquée(s) comme lue(s)."
            )
        
        notification_ids = serializer.validated_data.get('notification_ids', [])
        if notification_ids:
            Notification.objects.filter(
                user=request.user,
                id__in=notification_ids
            ).update(is_read=True)
            return APIResponse.success(
                message=f"{len(notification_ids)} notification(s) marquée(s) comme lue(s)."
            )
        
        return APIResponse.error(
            message="Aucune notification à marquer.",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = NotificationService.get_unread_count(request.user)
        return APIResponse.success(data={'count': count})

