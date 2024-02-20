from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from trioapi.models import JournalTasks
from trioapi.serializers import JournalTasksSerializer

class JournalTaskView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requestt for single journal task
        """
        try:
            journal_task = JournalTasks.objects.get(pk=pk)
            serializer = JournalTasksSerializer(journal_task)
            return Response(serializer.data)
        except JournalTasks.DoesNotExist as ex:
            return Response({'message': ex.args [0]}, status = status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET reqeust for all journal tasks"""
    
        journal_tasks = JournalTasks.objects.all()
        serializer = JournalTasksSerializer(journal_tasks, many=True)
        return Response(serializer.data)
