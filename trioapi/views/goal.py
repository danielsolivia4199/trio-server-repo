from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from trioapi.models import Goal
from trioapi.serializers import GoalSerializer

class GoalView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requestt for single goal
        """
        try:
            goal = Goal.objects.get(pk=pk)
            serializer = GoalSerializer(goal)
            return Response(serializer.data)
        except Goal.DoesNotExist as ex:
            return Response({'message': ex.args [0]}, status = status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET reqeust for all task"""
    
        goals = Goal.objects.all()
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)
