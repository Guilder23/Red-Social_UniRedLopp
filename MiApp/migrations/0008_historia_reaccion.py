# Generated by Django 5.1.1 on 2025-01-06 20:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MiApp', '0007_mensaje'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Historia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='historias/')),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_expiracion', models.DateTimeField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historias', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaccion', models.CharField(choices=[('like', 'Me gusta'), ('dislike', 'No me gusta')], max_length=10)),
                ('historia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reacciones', to='MiApp.historia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('historia', 'usuario')},
            },
        ),
    ]
