from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from trioapi.models import Journal
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
