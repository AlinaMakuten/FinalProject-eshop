# Generated by Django 4.1.3 on 2022-12-06 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_reviewrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewrating',
            name='subject',
        ),
    ]
