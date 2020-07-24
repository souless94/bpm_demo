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
    path('warnings/',views.post_warnings),
    path('swo/',views.post_SWO),
    path('vet_approve/<int:id>/',views.get_vetApproveAction,name='vet_approve'),
    path('vet_approve/',views.post_vetApproveAction),
    path('approve/<int:id>/',views.get_Approve,name='approve'),
    path('approve/',views.post_Approve),
    path('enforcement/',views.post_enforcement),
    path('resume/',views.post_resume)
    # path('approve/',views.submit),
    # path('resume/',views.resume),
]