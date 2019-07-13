from django.urls import path

from . import views
from scheduler.views import JobJSONView

app_name = 'faststi'

urlpatterns = [
    path('', views.FaststiFormView.as_view(), name='faststi_form'),
    path('fetch', JobJSONView.as_view(), name='faststi_fetch'),
    path('config/<slug>/', views.show_config_file, name='faststi_config'),
    path('data/<slug>/', views.show_data_file, name='faststi_data'),
    path('output/<slug>/', views.show_output_file, name='faststi_output'),
]
