# Generated by Django 3.1.2 on 2020-10-14 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('genres', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.TextField(max_length=300, unique=True)),
                ('imdb', models.FloatField()),
                ('classification', models.IntegerField()),
                ('year', models.IntegerField()),
                ('description', models.TextField()),
                ('downloads', models.IntegerField(default=0)),
                ('created', models.DateTimeField()),
                ('genres', models.ManyToManyField(to='genres.Genre')),
            ],
        ),
    ]
