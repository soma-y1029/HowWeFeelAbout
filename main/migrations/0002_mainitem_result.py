# Generated by Django 2.1 on 2020-10-26 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainitem',
            name='result',
            field=models.IntegerField(default=80),
        ),
    ]