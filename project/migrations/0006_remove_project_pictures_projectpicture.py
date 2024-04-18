# Generated by Django 5.0.3 on 2024-04-14 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_featuredproject_delete_activationlink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='pictures',
        ),
        migrations.CreateModel(
            name='ProjectPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='project_pictures/%Y/%m/%d')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
        ),
    ]
