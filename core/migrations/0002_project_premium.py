# Generated by Django 3.0.3 on 2020-11-24 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='premium',
            field=models.BooleanField(default=True),
        ),
    ]