# Generated by Django 5.0.6 on 2024-06-18 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0006_producto_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carroitem',
            name='usuario',
        ),
        migrations.AddField(
            model_name='carroitem',
            name='usuario_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]