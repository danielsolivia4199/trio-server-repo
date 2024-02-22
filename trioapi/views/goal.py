from django.http import HttpResponseServerError
from django.utils import timezone
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from trioapi.models import Goal, User, Category
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
        """Handle GET reqeust for all goal"""
    
        goals = Goal.objects.all()
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        """Handle DESTROY requests for goal

        Returns:
            Response -- Empty body with 204 status code
        """
        goal = Goal.objects.get(pk=pk)
        goal.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized goal instance
        """
        user = User.objects.get(pk=request.data["user"])
        category = Category.objects.get(pk=request.data["category"])

        goal = Goal.objects.create(
            user=user,
            category=category,
            goal=request.data["goal"],
            goal_created=request.data["goalCreated"],
            complete=request.data["complete"],
            completed_on=request.data["completedOn"]
        )
        serializer = GoalSerializer(goal)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a goal, allowing only the goal field to be updated.

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            goal = Goal.objects.get(pk=pk)
            goal.goal = request.data.get("goal", goal.goal)
            goal.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Goal.DoesNotExist:
            return Response({'error': 'Goal not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['post'], detail=True, url_path='complete-goal')
    def complete_goal(self, request, pk=None):
        """Mark a goal as complete and log the completion time."""
        try:
            goal = Goal.objects.get(pk=pk)
            goal.complete = True
            goal.completed_on = timezone.now()
            goal.save()

            serializer = GoalSerializer(goal, context={'request': request})
            return Response(serializer.data)
        except Goal.DoesNotExist:
            return Response({'error': 'Goal not found'}, status=status.HTTP_404_NOT_FOUND)
