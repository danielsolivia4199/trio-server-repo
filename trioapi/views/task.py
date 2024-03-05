from django.db import transaction
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
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
        """Handle GET request for all tasks, with optional filtering by category and completion status."""
        tasks = Task.objects.all()
        
        category = request.query_params.get('category', None)
        if category is not None:
            tasks = tasks.filter(category_id=category)

        complete = request.query_params.get('complete', None)
        if complete is not None:
            if complete == '0':
                tasks = tasks.filter(complete=False)
            elif complete == '1':
                tasks = tasks.filter(complete=True)

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
        category_id = request.data.get("category")
        if category_id:
            category_instance = get_object_or_404(Category, pk=category_id)
            task.category = category_instance
        else:
            task.category = task.category
        task.task = request.data.get("task", task.task)
        task.difficulty = request.data.get("difficulty", task.difficulty)
        task.repeat = request.data.get("repeat", task.repeat)
        
        task.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='start-trio')
    def start_new_trio(self, request):
        try:
            # Select three tasks with difficulty levels 1, 2, and 3 that are not complete and trio is 0
            tasks = Task.objects.filter(difficulty__in=[1, 2, 3], complete=False, trio=0)[:3]

            # Check if we have exactly 3 tasks, one of each difficulty level
            if tasks.count() != 3:
                return Response({"error": "Insufficient tasks available for a new trio."}, status=400)

            for task in tasks:
                task.trio = 1
                task.save()

            serializer = TaskSerializer(tasks, many=True)

            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

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
    
    @action(detail=False, methods=['get'])
    def trio_tasks(self, request):
        """Handle GET request for trio tasks."""
        trio_tasks = Task.objects.filter(trio=1)
        serializer = TaskSerializer(trio_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='complete-trio')
    def complete_trio_tasks(self, request):
        """Completes all trio tasks."""
        try:
            trio_tasks = Task.objects.filter(trio=True)
            trio_tasks.update(complete=True, trio=False)
            return Response({"message": "Trio tasks completed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='tasks-by-category')
    def get_tasks_by_category(self, request):
        category_id = request.GET.get('category')
        complete = request.GET.get('complete', '0')

        if not category_id:
            return Response({'error': 'No category ID provided'}, status=400)

        tasks = Task.objects.filter(category_id=category_id, complete=complete)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
