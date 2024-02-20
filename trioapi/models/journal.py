from django.db import models
from .goal import Goal
from .user import User
from .task import Task

class Journal(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_thoughts = models.TextField()
    hardest_tasks = models.ManyToManyField(Task, through='JournalTasks')
    task_reflection = models.TextField()
    learned = models.TextField()
    do_differently = models.TextField()
    take_away = models.TextField()
