# Generated by Django 3.2.5 on 2022-01-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='time',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]