from django.db import models
from .user import User
from .category import Category

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    goal = models.TextField(blank=True, null=True)
    goal_created = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField()
    completed_on = models.DateTimeField(null=True, blank=True)
