from rest_framework import serializers
from trioapi.models import Task
from .category import CategorySerializer


class TaskSerializer(serializers.ModelSerializer):
    """JSON serializer for Tasks"""

    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'user', 'category', 'task', 'difficulty', 'repeat', 'trio', 'complete')
        depth = 1
