# Generated by Django 3.1.7 on 2021-04-05 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0008_auto_20210404_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='activity',
            field=models.CharField(choices=[('BP', 'Backpacking'), ('SS', 'Siteseeing'), ('LS', 'Leisure'), ('BS', 'Business')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='season',
            field=models.CharField(choices=[('WT', 'Winter'), ('SP', 'Spring'), ('SM', 'Summer'), ('FL', 'Fall')], max_length=2),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('date', models.DateField(verbose_name=' Date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='My_Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.item')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.trip')),
            ],
        ),
    ]
