# Generated by Django 3.1.2 on 2020-10-17 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership_type',
            field=models.CharField(choices=[('Monthly', 'monthly'), ('Daily', 'daily'), ('Free', 'free')], default='Free', max_length=30),
        ),
    ]
