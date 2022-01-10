# Generated by Django 4.0.1 on 2022-01-10 17:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique id for this particular template.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Must be a python error class, e.g. TypeError', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ErrorTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique id for this particular template.', primary_key=True, serialize=False)),
                ('template', models.CharField(help_text='Paste your error trace here!', max_length=400)),
                ('error_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='results.errortype')),
            ],
        ),
    ]