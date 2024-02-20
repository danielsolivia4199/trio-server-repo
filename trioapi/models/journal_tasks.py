from django.db import models
from .task import Task
from .journal import Journal

class JournalTasks(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='journal_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_journals')
