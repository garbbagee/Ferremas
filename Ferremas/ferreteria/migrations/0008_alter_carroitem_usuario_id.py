# Generated by Django 5.0.6 on 2024-06-18 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0007_remove_carroitem_usuario_carroitem_usuario_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carroitem',
            name='usuario_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
