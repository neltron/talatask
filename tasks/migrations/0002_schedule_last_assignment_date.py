# Generated by Django 5.1.3 on 2024-11-06 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='last_assignment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]