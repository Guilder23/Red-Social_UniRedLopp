from django.db import models

# Create your models here.
from django.contrib.auth.models import User

#Para historias
from datetime import timedelta
from django.utils import timezone

from datetime import date

class Publicacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones')
    contenido = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='publicaciones/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    me_gusta = models.ManyToManyField(User, related_name='me_gusta', blank=True)

    def total_me_gusta(self):
        return self.me_gusta.count()

    def __str__(self):
        return f'Publicación de {self.usuario.username} - {self.fecha_creacion}'


# Modelo para los "Me gusta"
class MeGusta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} le dio like a la publicación {self.publicacion.id}'

# Modelo para los comentarios--------------------------------------------------------------------------------------------
class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario.username} en {self.publicacion.id}'


#MI PERFIL-----------------------------------------------------------------------------------------------------------
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Información adicional sobre el usuario
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)  # Foto de perfil

    def __str__(self):
        return self.usuario.username


#AMIGOS------------------------------------------------------------------------------------------------------------

class Amistad(models.Model):
    usuario1 = models.ForeignKey(User, related_name='amigos', on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(User, related_name='amigos_contra', on_delete=models.CASCADE)
    fecha_amigos = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario1', 'usuario2')

    def __str__(self):
        return f"{self.usuario1.username} y {self.usuario2.username} son amigos"

class Seguimiento(models.Model):
    seguidor = models.ForeignKey(User, related_name='seguidores', on_delete=models.CASCADE)
    seguido = models.ForeignKey(User, related_name='seguidos', on_delete=models.CASCADE)
    fecha_seguimiento = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seguidor', 'seguido')

    def __str__(self):
        return f"{self.seguidor.username} sigue a {self.seguido.username}"


#CONVERSASION Y MENSAJES

class Mensaje(models.Model):
    emisor = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.emisor.username} a {self.receptor.username}: {self.contenido[:50]}..."

#Nuevos agregados para enviar mensajes

#AGREGAR HISTORIAS------------------------------------------------------------------------------------------

# Modelo para la Historia
from django.db import models
from django.utils import timezone


class Historia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='historias/', blank=True, null=True)
    fecha_expiracion = models.DateField(default=date.today)

    def __str__(self):
        return f"Historia de {self.usuario.username}"


class Reaccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    historia = models.ForeignKey(Historia, related_name='reacciones_usuario', on_delete=models.CASCADE)
    tipo_reaccion = models.CharField(
        max_length=12,
        choices=[('like', 'Me gusta'), ('dislike', 'No me gusta')],
        default='like'  # Definir un valor por defecto
    )

    def __str__(self):
        return f"Reacción de {self.usuario.username} a la historia"
