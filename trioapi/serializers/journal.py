from rest_framework import serializers
from trioapi.models import Journal, Task
from .goal import GoalSerializer
from .task import TaskSerializer


class JournalSerializer(serializers.ModelSerializer):
    goal = GoalSerializer(read_only=True)
    hardest_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Journal
        fields = ('id', 'goal', 'user', 'initial_thoughts', 'hardest_tasks', 'task_reflection', 'learned', 'do_differently', 'take_away')
        depth = 1

    def get_hardest_tasks(self, obj):
        tasks = [jt.task for jt in obj.journal_tasks.all()]
        return TaskSerializer(tasks, many=True).data
