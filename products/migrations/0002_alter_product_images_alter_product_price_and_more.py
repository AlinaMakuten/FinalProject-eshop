# Generated by Django 4.1.3 on 2022-11-21 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ImageField(upload_to='media/photos/products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_description',
            field=models.TextField(blank=True, max_length=4600),
        ),
    ]
