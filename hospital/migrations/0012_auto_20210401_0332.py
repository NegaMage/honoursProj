# Generated by Django 3.1.7 on 2021-04-01 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0011_auto_20210401_0147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manuf_making',
            old_name='sold',
            new_name='cleared',
        ),
    ]
