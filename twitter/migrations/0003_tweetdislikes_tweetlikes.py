# Generated by Django 2.1.7 on 2019-03-23 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0002_tweet'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetDislikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitter.Tweet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitter.User')),
            ],
        ),
        migrations.CreateModel(
            name='TweetLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitter.Tweet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitter.User')),
            ],
        ),
    ]