from django.shortcuts import render
from  django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import Article

# Create your views here.

class HomeView(TemplateView):
    template_name = 'blog/home.html'

class HomeView(TemplateView):
    template_name = 'blog/home.html'

class ArticleListView(ListView):

    def get_queryset(self):
        return Article.objects.published()
    model = Article
    template_name = 'blog/list.html'

class ArticleDetailView(DetailView):
    pass
    # template_name = 'blog/detail.html'

def article_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.user.is_staff and article.is_published is False:
        messages.add_message(request, messages.INFO,
                             "This article is not published.")
    elif request.user.is_staff is False and article.is_published is False:
        raise Http404
    title_bar = str(article.slug).replace("_", " ")
    title_bar = title_bar.replace("-"," ").title()

    return render(request, article.template,
                  {'title_bar': title_bar, 'article': article})




class AboutView(TemplateView):
    template_name = 'blog/about.html'

class CvView(TemplateView):
    template_name = 'blog/cv.html'
