# Generated by Django 3.1.7 on 2021-04-04 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]