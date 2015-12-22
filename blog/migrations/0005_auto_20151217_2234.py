# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20151217_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='likeforanswer',
            name='answer',
            field=models.ForeignKey(to='blog.Answer', null=True),
        ),
        migrations.AddField(
            model_name='likeforquestion',
            name='question',
            field=models.ForeignKey(to='blog.Question', null=True),
        ),
    ]
