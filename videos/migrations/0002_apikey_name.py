# Generated by Django 2.2.6 on 2020-08-24 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='name',
            field=models.CharField(default='Youtube API', max_length=255),
        ),
    ]
