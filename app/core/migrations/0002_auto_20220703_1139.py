# Generated by Django 3.2.13 on 2022-07-03 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personel',
            name='department',
        ),
        migrations.RemoveField(
            model_name='personel',
            name='position',
        ),
        migrations.AddField(
            model_name='personel',
            name='birthday',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('coordinator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.personel')),
            ],
        ),
    ]
