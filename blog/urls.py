from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('list/', views.ArticleListView.as_view(), name='list'),
    path('article/<slug>/', views.ArticleDetailView.as_view(), name='detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('nathan/', views.CvView.as_view(), name='cv')
]
