from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('state', views.StateViewSet)
router.register('processForm', views.ProcessFormViewSet)

app_name = 'the_process'

urlpatterns = [
    path('', include(router.urls))
]
