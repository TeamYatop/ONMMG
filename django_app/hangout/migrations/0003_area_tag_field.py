# Generated by Django 2.0.2 on 2018-03-14 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangout', '0002_auto_20180313_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='tag_field',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
