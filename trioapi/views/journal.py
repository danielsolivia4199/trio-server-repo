from django.http import HttpResponseServerError
from django.db import transaction
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
        with transaction.atomic():
            user = User.objects.get(pk=request.data["user"])
            goal = Goal.objects.get(pk=request.data["goal"])

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
            for task_id in hardest_tasks_ids:
                task = Task.objects.get(pk=task_id)
                JournalTasks.objects.create(journal=journal, task=task)

            serializer = JournalSerializer(journal, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
