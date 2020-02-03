from django.shortcuts import render
from  django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.contrib import messages

from .models import Article

# Create your views here.

class HomeView(TemplateView):
    template_name = 'blog/home.html'

class HomeView(TemplateView):
    template_name = 'blog/home.html'

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/list.html'

    def get_queryset(self):
        return Article.objects.published()

class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        if self.request.user.is_staff is False:
            if article.is_published() is False:
                raise Http404

        if article.is_published() is False:
            messages.add_message(self.request, messages.INFO,
                                 "This article is not published.")
        return article

    def get_template_names(self):
        return self.object.template

    def  get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["title_bar"] = str(self.object.slug).replace("-"," ").\
                               replace("_", " ")
        return context

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class CvView(TemplateView):
    template_name = 'blog/cv.html'
