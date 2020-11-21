from django.urls import path

from . import views

app_name = 'sudoku'

urlpatterns = [
    path('sudoku/latest/', views.SudokuLatest.as_view(), name='latest'),
    path('sudoku/<pk>/', views.SudokuDetailView.as_view(), name='detail'),
]
