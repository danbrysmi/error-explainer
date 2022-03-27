# Generated by Django 4.0.1 on 2022-03-27 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_errortype_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='errortemplate',
            name='short_desc',
            field=models.CharField(default='Come back for a description soon!', help_text='A brief description of the specific trace', max_length=800),
            preserve_default=False,
        ),
    ]
