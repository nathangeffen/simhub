from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog.urls')),
    path('', include('sudoku.urls')),
    path('gambler/', include('gambler.urls')),
    path('scheduler/', include('scheduler.urls')),
    path('faststi/', include('faststi.urls')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
