# Generated by Django 4.0.1 on 2022-01-20 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0008_rename_created_at_project_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='tags',
        ),
        migrations.AddField(
            model_name='tag',
            name='projects',
            field=models.ManyToManyField(blank=True, to='myproject.Project'),
        ),
    ]
