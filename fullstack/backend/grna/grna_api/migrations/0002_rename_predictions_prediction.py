# Generated by Django 4.2.7 on 2023-12-14 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grna_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Predictions',
            new_name='Prediction',
        ),
    ]