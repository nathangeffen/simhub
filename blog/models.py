from django.db import models
from django.utils import timezone
from django.urls import reverse

class ArticleQuerySet(models.QuerySet):

    def published(self):
        return self.filter(published__lte=timezone.now())

class Article(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    body = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    additional_header = models.TextField(blank=True)
    use_context_processor = models.BooleanField(default=True)
    stickiness = models.IntegerField(default=0)
    template = models.CharField(max_length=200, default="blog/detail.html")
    published = models.DateTimeField(blank=True, null=True,
                                     verbose_name='publish time')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    objects = ArticleQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.slug, ])

    def is_published(self):
        return (self.published is not None) and \
            (self.published <= timezone.now())

    def publish_now(self):
        if self.is_published() is False:
            self.published = timezone.now()
            self.save()

    is_published.boolean = True
    is_published.short_description = 'published'

    def __str__(self):
        return str(self.pk) + ": " + self.slug

    def unsticky(self):
        self.stickiness = 0
        self.save()

    class Meta:
        ordering = ["-stickiness", "-published", ]
