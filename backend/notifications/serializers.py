"""
Serializers for notifications
"""
from rest_framework import serializers
from core.notifications import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'type',
            'type_display',
            'title',
            'message',
            'is_read',
            'related_object_type',
            'related_object_id',
            'created_at',
            'read_at',
        ]
        read_only_fields = ['created_at', 'read_at']


class NotificationMarkReadSerializer(serializers.Serializer):
    """Serializer for marking notifications as read"""
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    mark_all = serializers.BooleanField(default=False)

