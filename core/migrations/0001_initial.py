# Generated by Django 3.1.2 on 2020-10-16 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('born', models.DateField()),
                ('height', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
    ]
