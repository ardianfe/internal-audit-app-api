# Generated by Django 3.2.14 on 2022-07-08 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_rename_standard_standardpoint_standard_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='cat',
            field=models.CharField(choices=[('MJ', 'Major'), ('MI', 'Minor'), ('OBSV', 'Observasi')], default='OBSV', max_length=4),
        ),
    ]
