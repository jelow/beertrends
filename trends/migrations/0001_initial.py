# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-04 01:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('beerdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(max_length=6)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=4)),
                ('date', models.DateField()),
                ('beer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beerdata.Beer')),
                ('brewery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beerdata.Brewery')),
            ],
        ),
    ]