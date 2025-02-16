# Generated by Django 5.1.3 on 2025-02-12 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_alter_product_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productunit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='inventario.productvariant'),
        ),
        migrations.AlterField(
            model_name='stockunit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_units', to='inventario.productvariant'),
        ),
    ]
