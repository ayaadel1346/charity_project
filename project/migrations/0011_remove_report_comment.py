# Generated by Django 5.0.3 on 2024-04-19 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_remove_comment_parent_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='comment',
        ),
    ]
