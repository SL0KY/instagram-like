# Generated by Django 2.2.7 on 2019-11-29 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='counter_views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
