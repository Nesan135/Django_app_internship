# Generated by Django 3.2.6 on 2021-09-01 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irdp', '0006_auto_20210830_0334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ahli',
            name='id',
        ),
        migrations.AlterField(
            model_name='ahli',
            name='state',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]