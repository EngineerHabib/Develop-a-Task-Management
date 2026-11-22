from django.urls import path
from TaskManager.views import *

urlpatterns = [
    path('', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('logout/', logout_view, name='logout_view'),
    path('dashboard/', dashboard_view, name='dashboard_view'),

    path('task-list/', task_list, name='task_list'),
    path('add-task/', add_task, name='add_task'),
    path('update-task/<str:id>/', update_task, name='update_task'),
    path('delete-task/<str:id>/', delete_task, name='delete_task'),
    path('complete-task/<str:id>/', complete_task, name='complete_task'),
]
