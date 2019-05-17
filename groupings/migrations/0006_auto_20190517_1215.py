# Generated by Django 2.1.5 on 2019-05-17 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groupings', '0005_auto_20190201_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(default='43.248949', max_length=50)),
                ('longitude', models.CharField(default='76.899709', max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='grouping',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='grouping',
            name='longitude',
        ),
        migrations.AddField(
            model_name='grouping',
            name='coordinates',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='groupings.Coordinate'),
        ),
    ]
