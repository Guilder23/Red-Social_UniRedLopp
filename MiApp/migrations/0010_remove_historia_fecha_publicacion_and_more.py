# Generated by Django 5.1.1 on 2025-01-06 20:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MiApp', '0009_alter_reaccion_unique_together_historia_reacciones_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historia',
            name='fecha_publicacion',
        ),
        migrations.RemoveField(
            model_name='historia',
            name='reacciones',
        ),
        migrations.AlterField(
            model_name='historia',
            name='fecha_expiracion',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
