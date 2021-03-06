# Generated by Django 2.1.5 on 2019-01-26 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouping',
            name='small_event_address',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grouping',
            name='small_event_city',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grouping',
            name='small_event_date',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grouping',
            name='small_event_desc',
            field=models.CharField(default=' ', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grouping',
            name='small_event_time',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grouping',
            name='small_min_people',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grouping',
            name='small_price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grouping',
            name='type',
            field=models.CharField(default=' ', max_length=50),
            preserve_default=False,
        ),
    ]
