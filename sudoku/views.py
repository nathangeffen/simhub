#from django.views.generic.base import TemplateView
#from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render
# from django.http import Http404
from django.contrib import messages

from sudoku.models import Sudoku

class SudokuDetailView(DetailView):
    model = Sudoku

    def get_object(self, queryset=None):
        sudoku = super().get_object(queryset)
        if self.request.user.is_staff is False:
            if sudoku.is_published() is False:
                raise Http404

        if sudoku.is_published() is False:
            messages.add_message(self.request, messages.INFO,
                                 "This Sudoku puzzle is not published.")
        return sudoku

    def  get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            context['next'] = Sudoku.objects.published(). \
                filter(published__gt=self.object.published).earliest('published')
        except Sudoku.DoesNotExist:
            context['next'] = None
        try:
            context['prev'] = Sudoku.objects.published(). \
                filter(published__lt=self.object.published).latest('published')
        except Sudoku.DoesNotExist:
            context['prev'] = None

        return context

class SudokuLatest(SudokuDetailView):

    def get_object(self, queryset=None):
        sudoku = Sudoku.objects.published().latest('published')
        return sudoku
