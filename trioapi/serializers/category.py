from rest_framework import serializers
from trioapi.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for Categories"""
    
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'goal_description', 'task_description', 'active')
