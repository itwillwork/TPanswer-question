# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20151124_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeForAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.BooleanField()),
                ('mark', models.BooleanField()),
                ('author', models.PositiveIntegerField()),
                ('numer', models.ForeignKey(to='blog.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='LikeForQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.BooleanField()),
                ('mark', models.BooleanField()),
                ('author', models.PositiveIntegerField()),
                ('numer', models.ForeignKey(to='blog.Profile')),
            ],
        ),
        migrations.RemoveField(
            model_name='like',
            name='numer',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
