# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 04:12
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.CharField(editable=False, max_length=256, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('desc', models.CharField(max_length=256)),
                ('ibu', models.PositiveSmallIntegerField()),
                ('abv', models.DecimalField(decimal_places=2, max_digits=4)),
                ('srm', models.PositiveSmallIntegerField()),
                ('og', models.DecimalField(decimal_places=2, max_digits=4)),
                ('fg', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.CharField(editable=False, max_length=256, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('lat', models.CharField(max_length=256)),
                ('lng', models.CharField(max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='styles',
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='fg',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(1.04)]),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='fuzziness',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.1000000000000000055511151231257827021181583404541015625'), max_digits=4, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='og',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(1.02), django.core.validators.MaxValueValidator(1.13)]),
        ),
        migrations.DeleteModel(
            name='Style',
        ),
        migrations.AddField(
            model_name='beer',
            name='brewery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.Brewery'),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='beers',
            field=models.ManyToManyField(to='recommender.Beer'),
        ),
    ]
