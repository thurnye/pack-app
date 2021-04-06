# Generated by Django 3.1.7 on 2021-04-06 13:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='person',
        ),
        migrations.AddField(
            model_name='item',
            name='age',
            field=models.CharField(choices=[('A', 'All Ages'), ('I', 'Infant'), ('C', 'Child'), ('T', 'Teen'), ('A', 'Adult'), ('S', 'Senior')], default='All Ages', max_length=25),
        ),
        migrations.AddField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='trip_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='traveler',
            name='age',
            field=models.CharField(choices=[('A', 'All Ages'), ('I', 'Infant'), ('C', 'Child'), ('T', 'Teen'), ('A', 'Adult'), ('S', 'Senior')], default='All Ages', max_length=25),
        ),
        migrations.AddField(
            model_name='traveler',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='traveler',
            name='gender',
            field=models.CharField(choices=[('A', 'All'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='All', max_length=25),
        ),
        migrations.AddField(
            model_name='traveler',
            name='trip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.trip'),
        ),
        migrations.AddField(
            model_name='traveler',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='activity',
            field=models.CharField(choices=[('AL', 'All'), ('BP', 'Backpacking'), ('SS', 'Sightseeing'), ('LS', 'Leisure'), ('BS', 'Business'), ('OT', 'Other')], default='All', max_length=25),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('CL', 'Clothing'), ('EL', 'Electronics'), ('EQ', 'Equipment'), ('PS', 'Personal'), ('MD', 'Medication'), ('OT', 'Other')], max_length=25),
        ),
        migrations.AlterField(
            model_name='item',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='item',
            name='country',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='item',
            name='gender',
            field=models.CharField(choices=[('A', 'All'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='All', max_length=25),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='item',
            name='season',
            field=models.CharField(choices=[('AL', 'All'), ('WT', 'Winter'), ('SP', 'Spring'), ('SM', 'Summer'), ('FL', 'Fall')], default='All', max_length=25),
        ),
        migrations.AlterField(
            model_name='trip',
            name='activity',
            field=models.CharField(default='All', max_length=50),
        ),
        migrations.AlterField(
            model_name='trip',
            name='season',
            field=models.CharField(choices=[('AL', 'All'), ('WT', 'Winter'), ('SP', 'Spring'), ('SM', 'Summer'), ('FL', 'Fall')], default='All', max_length=25),
        ),
        migrations.AlterField(
            model_name='trip',
            name='travelers',
            field=models.CharField(default='', max_length=50),
        ),
    ]