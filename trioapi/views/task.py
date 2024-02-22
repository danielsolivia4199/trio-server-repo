from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from trioapi.models import Task, User, Category
from trioapi.serializers import TaskSerializer

class TaskView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requestt for single task
        """
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist as ex:
            return Response({'message': ex.args [0]}, status = status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET request for all tasks, with optional filtering by category."""
        tasks = Task.objects.all()
        category = request.query_params.get('category', None)
        if category is not None:
            tasks = tasks.filter(category_id=category)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        """Handle DESTROY requests for task

        Returns:
            Response -- Empty body with 204 status code
        """
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized task instance
        """
        user = User.objects.get(pk=request.data["user"])
        category = Category.objects.get(pk=request.data["category"])

        task = Task.objects.create(
            user=user,
            category=category,
            task=request.data["task"],
            difficulty=request.data["difficulty"],
            repeat=request.data["repeat"],
            trio=request.data["trio"],
            complete=request.data["complete"]
        )
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for task

        Returns:
            Response -- Empty body with 204 status code
        """
        task = Task.objects.get(pk=pk)
        task.category = request.data.get("category", task.category)
        task.task = request.data.get("task", task.task)
        task.difficulty = request.data.get("difficulty", task.difficulty)
        task.repeat = request.data.get("repeat", task.repeat)
        
        task.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def start_new_trio(self, selected_task_ids):
        """
        Marks selected tasks as part of a new trio.
        This could be triggered by some internal logic or specific conditions.
        """
        tasks = Task.objects.filter(id__in=selected_task_ids)
        for task in tasks:
            task.trio = True
            task.save(update_fields=['trio'])
    
    @action(detail=True, methods=['patch'], url_path='mark-complete')
    def mark_complete(self, request, pk=None):
        """Marks a task as complete."""
        try:
            task = Task.objects.get(pk=pk)
            task.complete = True
            task.save(update_fields=['complete'])
            return Response({'status': 'Task marked as complete.'})
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
    