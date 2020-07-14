from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('state', views.StateViewSet)
router.register('createInspectionForm', views.CreateInspectionFormViewSet)
router.register('findingsForm', views.FindingsFormViewSet)
router.register('questionaireForm', views.QuestionaireFormViewSet)
router.register('warningsForm', views.WarningsFormViewSet)
router.register('swoForm', views.SWOFormViewSet)
router.register('approvalForm', views.ApprovalFormViewSet)

app_name = 'the_process'

urlpatterns = [
    path('', include(router.urls))
]
