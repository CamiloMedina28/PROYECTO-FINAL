# Generated by Django 5.0.3 on 2024-04-03 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_alter_persona_per_telefono'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consulta',
            options={'verbose_name': 'Consulta', 'verbose_name_plural': 'Consultas'},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'Material', 'verbose_name_plural': 'Materiales'},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterModelOptions(
            name='proveedor',
            options={'verbose_name': 'Proveedor', 'verbose_name_plural': 'Proveedores'},
        ),
        migrations.AlterField(
            model_name='producto',
            name='pro_img',
            field=models.ImageField(upload_to='products'),
        ),
    ]