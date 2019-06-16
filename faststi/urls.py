from django.urls import path

from . import views
from scheduler.views import JobJSONView

app_name = 'faststi'

urlpatterns = [
    path('', views.FaststiFormView.as_view(), name='faststi_form'),
    path('fetch', JobJSONView.as_view(), name='faststi_fetch'),
]
