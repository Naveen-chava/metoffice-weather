# Generated by Django 4.2.1 on 2023-05-22 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media_document', '0003_year_parameter_year_region_alter_year_year'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='year',
            unique_together={('region', 'parameter', 'year')},
        ),
    ]
