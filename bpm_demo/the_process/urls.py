from django.urls import path , include
from . import views

app_name = 'the_process'

urlpatterns = [
    path('',views.index ),
    path('submit/',views.start_execution),
    path('the_process/<int:id>',views.get_task,name='get_task'),
    path('approve/',views.submit),
]