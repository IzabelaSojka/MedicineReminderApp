# Generated by Django 3.2.5 on 2022-01-18 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20220118_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='mail',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
    ]
