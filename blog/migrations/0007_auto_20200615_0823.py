# Generated by Django 3.0.7 on 2020-06-15 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200614_2348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_author',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='reply',
            old_name='reply_author',
            new_name='author',
        ),
    ]
