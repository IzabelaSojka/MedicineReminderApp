# Generated by Django 3.2.5 on 2022-01-18 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20220118_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Notatka'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='leaflet',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ulotka'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='mail',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='time',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Godzina wzięcia'),
        ),
        migrations.AlterField(
            model_name='medicine_database',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nazwa Leku'),
        ),
    ]
