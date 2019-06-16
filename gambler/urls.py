from django.urls import path

from . import views
from scheduler.views import JobJSONView

app_name = 'gambler'

urlpatterns = [
    path('', views.GamblerFormView.as_view(), name='gambler_form'),
    path('fetch', JobJSONView.as_view(), name='gambler_fetch'),
]
