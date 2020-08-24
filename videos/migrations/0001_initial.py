# Generated by Django 2.2.6 on 2020-08-24 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('query_limit_per_day', models.PositiveIntegerField(default=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('description', models.TextField(blank=True, null=True)),
                ('youtube_video_id', models.CharField(max_length=100)),
                ('channel_name', models.CharField(max_length=500)),
                ('thumbnail_url', models.URLField()),
                ('published_at', models.DateTimeField()),
            ],
        ),
    ]
