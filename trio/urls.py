from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from trioapi.views import (
    register_user, 
    check_user, 
    CategoryView, 
    GoalView, 
    JournalTaskView, 
    JournalView, 
    TaskView,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView, 'category')
router.register(r'goals', GoalView, 'goal')
router.register(r'journal_tasks', JournalTaskView, 'journal_task')
router.register(r'journals', JournalView, 'journal')
router.register(r'tasks', TaskView, 'task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('checkuser', check_user)
]
