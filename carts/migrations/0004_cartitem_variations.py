# Generated by Django 4.1.3 on 2022-12-04 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_variation'),
        ('carts', '0003_cartitem_user_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='products.variation'),
        ),
    ]