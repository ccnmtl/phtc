# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pagetree', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info', models.TextField(default=b'')),
                ('dashboard', models.OneToOneField(to='pagetree.Section')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModuleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info', models.TextField(default=b'')),
                ('module_type', models.OneToOneField(to='pagetree.Section')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NYLEARNS_Course_Map',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('courseID', models.TextField()),
                ('phtc_url', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SectionCss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('css_field', models.TextField()),
                ('section_css', models.OneToOneField(to='pagetree.Section')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fname', models.TextField()),
                ('lname', models.TextField()),
                ('work_city', models.TextField()),
                ('work_state', models.TextField()),
                ('work_zip', models.TextField()),
                ('sex', models.TextField()),
                ('age', models.TextField()),
                ('origin', models.TextField()),
                ('ethnicity', models.TextField()),
                ('umc', models.TextField(default=b'')),
                ('employment_location', models.TextField()),
                ('other_employment_location', models.TextField()),
                ('position', models.TextField()),
                ('other_position_category', models.TextField()),
                ('dept_health', models.TextField()),
                ('geo_dept_health', models.TextField()),
                ('experience', models.TextField()),
                ('rural', models.TextField()),
                ('degree', models.TextField()),
                ('disadvantaged', models.TextField()),
                ('is_nylearns', models.BooleanField(default=False)),
                ('nylearns_course_init', models.TextField(default=b'none')),
                ('nylearns_user_id', models.TextField(default=b'none')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
