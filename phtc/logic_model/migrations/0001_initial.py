# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivePhase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ['game_phase', 'column'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BoxColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=256)),
                ('color', models.CharField(default=b'FFFFFF', max_length=6)),
                ('order_rank', models.IntegerField(default=0, null=True, blank=True)),
            ],
            options={
                'ordering': ['order_rank'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=256)),
                ('order_rank', models.IntegerField(default=0, null=True, blank=True)),
                ('css_classes', models.CharField(default=b'', max_length=256, null=True, blank=True)),
                ('help_definition', models.TextField(default=b'', null=True, blank=True)),
                ('help_examples', models.TextField(default=b'', null=True, blank=True)),
                ('flavor', models.CharField(default=b'', max_length=256)),
            ],
            options={
                'ordering': ['order_rank'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GamePhase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=256)),
                ('instructions', models.TextField(default=b'', null=True, blank=True)),
                ('order_rank', models.IntegerField(default=0, null=True, blank=True)),
                ('css_classes', models.CharField(default=b'', max_length=256, null=True, blank=True)),
            ],
            options={
                'ordering': ['order_rank'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogicModelBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=256)),
                ('difficulty', models.CharField(default=b'', max_length=256)),
                ('order_rank', models.IntegerField(default=0, null=True, blank=True)),
                ('instructions', models.TextField(default=b'', null=True, blank=True)),
            ],
            options={
                'ordering': ['order_rank'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activephase',
            name='column',
            field=models.ForeignKey(to='logic_model.Column'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activephase',
            name='game_phase',
            field=models.ForeignKey(to='logic_model.GamePhase'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='activephase',
            unique_together=set([('game_phase', 'column')]),
        ),
    ]
