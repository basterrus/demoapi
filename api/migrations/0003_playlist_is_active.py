# Generated by Django 3.2.11 on 2022-01-20 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220120_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
