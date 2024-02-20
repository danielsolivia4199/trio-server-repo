from django.db import models

class Category(models.Model):
    category_name = models.TextField()
    goal_description = models.TextField()
    task_description = models.TextField()
    active = models.BooleanField()
  
