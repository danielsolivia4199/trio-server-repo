from rest_framework import serializers
from trioapi.models import JournalTasks
from .journal import JournalSerializer
from .task import TaskSerializer

class JournalTasksSerializer(serializers.ModelSerializer):
    journal = JournalSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    
    class Meta:
        model = JournalTasks
        fields = ('id', 'journal', 'task')
