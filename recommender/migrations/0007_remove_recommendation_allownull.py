# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-29 20:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0006_recommendation_allownull'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='allowNull',
        ),
    ]
