# Generated by Django 2.1.7 on 2019-03-23 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_tweetdislikes_tweetlikes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweetdislikes',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='tweetdislikes',
            name='user',
        ),
        migrations.DeleteModel(
            name='TweetDislikes',
        ),
    ]
