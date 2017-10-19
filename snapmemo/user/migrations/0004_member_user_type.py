# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_member_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='user_type',
            field=models.CharField(choices=[('normal', 'Normal'), ('facebook', 'Facebook')], default='normal', max_length=10),
        ),
    ]