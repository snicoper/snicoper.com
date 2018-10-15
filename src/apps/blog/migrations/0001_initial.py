# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 09:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Titulo')),
                ('slug', models.SlugField(blank=True, help_text='Si se quiere auto-generar otro slug, dejarlo en blanco.', max_length=255, unique=True)),
                ('image_header', models.ImageField(blank=True, null=True, upload_to='articles/headers', verbose_name='Imagen cabecera')),
                ('body', models.TextField(verbose_name='Cuerpo')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('views', models.IntegerField(default=0, verbose_name='Vistas')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Fecha modificación')),
            ],
            options={
                'verbose_name': 'Articulo',
                'verbose_name_plural': 'artículos',
                'ordering': ('-create_at',),
            },
        ),
        migrations.CreateModel(
            name='ArticleSubscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('token_unsigned', models.CharField(max_length=30, unique=True, verbose_name='Token unregister')),
            ],
            options={
                'verbose_name': 'Subscrito a artículos',
                'verbose_name_plural': 'Subscritos a artículos',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Titulo')),
                ('slug', models.SlugField(blank=True, help_text='Si se quiere auto-generar otro slug, dejarlo en blanco.', max_length=255, unique=True)),
                ('views', models.IntegerField(default=0, verbose_name='Vistas')),
                ('thumbnail', models.ImageField(upload_to='articles/tags', verbose_name='Miniatura')),
            ],
            options={
                'verbose_name': 'Etiqueta',
                'verbose_name_plural': 'Etiquetas',
                'ordering': ('-views',),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='default_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_default_tag', to='blog.Tag', verbose_name='Etiqueta principal'),
        ),
        migrations.AddField(
            model_name='article',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_owner', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_name='article_tags', to='blog.Tag', verbose_name='Etiquetas'),
        ),
    ]
