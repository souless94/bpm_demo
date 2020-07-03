from django.urls import path , include
from . import views

app_name = 'the_process'

urlpatterns = [
    path('',views.index ),
    path('submit/', views.submit),
    path('start_execution/', views.start_execution),
    path('get_task/<str:taskId>/', views.get_task, name='get_task')
]