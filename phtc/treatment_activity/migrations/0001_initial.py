# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TreatmentActivityBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TreatmentNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=2, choices=[(b'RT', b'Root'), (b'PR', b'Parent'), (b'IF', b'TreatmentStep'), (b'DP', b'DecisionPoint'), (b'ST', b'Stop')])),
                ('text', models.TextField(null=True, blank=True)),
                ('help', models.TextField(null=True, blank=True)),
                ('duration', models.IntegerField(default=0)),
                ('value', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TreatmentPath',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('cirrhosis', models.BooleanField(default=False)),
                ('treatment_status', models.IntegerField(choices=[(0, b'Treatment Naive'), (1, b'Prior Null Responder'), (2, b'Prior Relapser'), (3, b'Prior Partial Responder')])),
                ('drug_choice', models.CharField(max_length=12, choices=[(b'boceprevir', b'Boceprevir'), (b'telaprevir', b'Telaprevir')])),
                ('tree', models.ForeignKey(to='treatment_activity.TreatmentNode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
