from django.urls import path , include
from . import views

app_name = 'the_process'

urlpatterns = [
    path('',views.index ),
    path('createInspectionPage/',views.CreateInspectionPage),
    path('createInspection/',views.CreateInspection),
    path('update_inspection/<int:id>/',views.get_task,name='update_inspection'),
    path('updateInspection/',views.updateInspection),
    path('finding/<int:id>/',views.get_finding,name='finding'),
    path('findings/',views.post_finding),
    path('question/<int:id>/',views.get_questionaire,name='question'),
    path('question/',views.post_questionaire,),
    path('enforcement/<int:id>/',views.get_enforcement,name='enforcement'),
    path('enforcement/',views.post_enforcement),
    path('vet_approve/<int:id>/',views.get_vetApproveAction,name='vet_approve'),
    # path('approve/',views.submit),
    # path('resume/',views.resume),
]