# Generated by Django 5.1.3 on 2025-02-13 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_alter_productunit_product_alter_stockunit_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productunit',
            name='more_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
