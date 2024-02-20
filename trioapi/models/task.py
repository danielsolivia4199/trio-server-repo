from django.db import models
from .user import User
from .category import Category

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    task = models.TextField()
    difficulty = models.IntegerField()
    repeat = models.BooleanField()
    trio = models.BooleanField()
    complete = models.BooleanField()

  
