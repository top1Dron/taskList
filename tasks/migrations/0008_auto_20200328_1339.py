# Generated by Django 2.2.10 on 2020-03-28 11:39

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('tasks', '0007_todoitem_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuTag',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('taggit.tag',),
        ),
        migrations.CreateModel(
            name='RuTaggedItem',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('taggit.taggeditem',),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='tasks.RuTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]