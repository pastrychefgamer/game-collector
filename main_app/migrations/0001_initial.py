# Generated by Django 3.0.4 on 2020-03-26 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=250)),
                ('rating', models.IntegerField()),
            ],
        ),
    ]
