# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_ans', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('rating', models.IntegerField()),
                ('correct', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.BooleanField()),
                ('mark', models.BooleanField()),
                ('author', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(max_length=200, upload_to=b'')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('text_qest', models.TextField()),
                ('count_ans', models.PositiveIntegerField()),
                ('rating', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(to='blog.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='blog.Tags'),
        ),
        migrations.AddField(
            model_name='like',
            name='numer',
            field=models.ForeignKey(to='blog.Profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(to='blog.Profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='blog.Question'),
        ),
    ]
