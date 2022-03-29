# Generated by Django 4.0.1 on 2022-03-29 09:38

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('results', '0006_alter_errortemplate_error_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Title of tip', max_length=50)),
                ('desc', models.CharField(help_text='Tip main text', max_length=800)),
                ('link', models.CharField(help_text='Link to resource', max_length=400)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_wrong', models.CharField(help_text='Incorrect code example.', max_length=800)),
                ('code_right', models.CharField(help_text='Correct code example.', max_length=800)),
                ('desc_wrong', models.CharField(help_text='Why does the incorrect code not work?', max_length=800)),
                ('desc_right', models.CharField(help_text='Why does the correct code work?', max_length=800)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
