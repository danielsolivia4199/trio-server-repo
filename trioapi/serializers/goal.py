from rest_framework import serializers
from trioapi.models import Goal
from .category import CategorySerializer


class GoalSerializer(serializers.ModelSerializer):
    """JSON serializer for Tasks"""

    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Goal
        fields = ('id', 'user', 'category', 'goal', 'goal_created', 'complete', 'completed_on')
        depth = 1
