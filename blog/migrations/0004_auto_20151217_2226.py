# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20151217_2135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likeforanswer',
            name='entity',
        ),
        migrations.RemoveField(
            model_name='likeforanswer',
            name='numer',
        ),
        migrations.RemoveField(
            model_name='likeforquestion',
            name='entity',
        ),
        migrations.RemoveField(
            model_name='likeforquestion',
            name='numer',
        ),
        migrations.AlterField(
            model_name='likeforanswer',
            name='author',
            field=models.ForeignKey(to='blog.Profile'),
        ),
        migrations.AlterField(
            model_name='likeforanswer',
            name='mark',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='likeforquestion',
            name='author',
            field=models.ForeignKey(to='blog.Profile'),
        ),
        migrations.AlterField(
            model_name='likeforquestion',
            name='mark',
            field=models.IntegerField(),
        ),
    ]
