# Generated by Django 3.1.7 on 2021-04-05 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_auto_20210405_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]