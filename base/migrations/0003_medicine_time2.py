# Generated by Django 3.2.5 on 2022-01-10 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_medicine_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='time2',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
