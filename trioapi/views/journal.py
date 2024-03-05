from django.http import HttpResponseServerError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from trioapi.models import Journal, User, Goal, Task, JournalTasks
from trioapi.serializers import JournalSerializer

class JournalView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requestt for single journal
        """
        try:
            journal = Journal.objects.get(pk=pk)
            serializer = JournalSerializer(journal)
            return Response(serializer.data)
        except Journal.DoesNotExist as ex:
            return Response({'message': ex.args [0]}, status = status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET reqeust for all journal"""
    
        journals = Journal.objects.all()
        serializer = JournalSerializer(journals, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations for Journal, including setting hardest_tasks."""
        try:
            user = get_object_or_404(User, pk=request.data["user"])
            goal = get_object_or_404(Goal, pk=request.data["goal"])

            journal = Journal.objects.create(
                user=user,
                goal=goal,
                initial_thoughts=request.data.get("initialThoughts"),
                task_reflection=request.data.get("taskReflection"),
                learned=request.data.get("learned"),
                do_differently=request.data.get("doDifferently"),
                take_away=request.data.get("takeAway")
            )

            hardest_tasks_ids = request.data.get("hardestTasks", [])
            if hardest_tasks_ids:
                tasks = Task.objects.filter(pk__in=hardest_tasks_ids)
                journal_tasks = [JournalTasks(journal=journal, task=task) for task in tasks]
                JournalTasks.objects.bulk_create(journal_tasks)  
                
            serializer = JournalSerializer(journal, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
