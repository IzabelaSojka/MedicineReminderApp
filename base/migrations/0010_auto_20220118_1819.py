# Generated by Django 3.2.5 on 2022-01-18 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_medicine_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine_database',
            name='leaflet',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ulotka'),
        ),
        migrations.AlterField(
            model_name='medicine_database',
            name='active_substance',
            field=models.CharField(max_length=255, verbose_name='Substancja aktywna'),
        ),
    ]