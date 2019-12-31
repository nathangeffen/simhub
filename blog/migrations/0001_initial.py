# Generated by Django 3.0.1 on 2019-12-28 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('body', models.TextField(blank=True)),
                ('summary', models.TextField(blank=True)),
                ('additional_header', models.TextField(blank=True)),
                ('use_context_processor', models.BooleanField(default=True)),
                ('stickiness', models.IntegerField(default=0)),
                ('template', models.CharField(default='article.html', max_length=200)),
                ('published', models.DateTimeField(blank=True, null=True, verbose_name='publish time')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-stickiness', '-published'],
            },
        ),
    ]