from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from .models import Publicacion, MeGusta, Comentario
from django.contrib.auth.decorators import login_required
from .forms import PublicacionForm, ComentarioForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from .models import Publicacion

from .models import Perfil
from .forms import PerfilForm

from django.contrib import messages

from django.shortcuts import redirect
from django.contrib.auth import logout


from django.contrib.auth.models import User
from .models import Perfil, Amistad, Seguimiento

from django.shortcuts import render, redirect, get_object_or_404

from .models import Mensaje
from django.db.models import Q

#AGRGEGAR HISTORIA
from django.utils import timezone
from .models import Historia, Reaccion
from .forms import HistoriaForm
from django.http import Http404

from django.utils.timezone import now

from django.db.models import Count, Q

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Crea el usuario
            auth_login(request, user)  # Inicia sesión automáticamente
            return redirect('inicio')  # Redirige al inicio
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

#----------------------------------------------------------------------------------------------------------------------
# Vista para la página de inicio (feed de publicaciones)
def inicio(request):
    publicaciones = Publicacion.objects.all().order_by('-fecha_creacion')  # Mostrar las más recientes primero
    return render(request, 'inicio.html', {'publicaciones': publicaciones})

# Vista para agregar una nueva publicación
@login_required
def agregar_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_publicacion = form.save(commit=False)
            nueva_publicacion.usuario = request.user
            nueva_publicacion.save()
            return redirect('inicio')
    else:
        form = PublicacionForm()
    return render(request, 'agregar_publicacion.html', {'form': form})

# Vista para comentar una publicación
@login_required
def comentar(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.publicacion = publicacion
            comentario.save()
            return redirect('inicio')
    else:
        form = ComentarioForm()
    return render(request, 'comentar.html', {'form': form, 'publicacion': publicacion})


#PUBLICACION-----------------------------------------------------------------------------------------------------
@login_required
def agregar_publicacion(request):
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        imagen = request.FILES.get('imagen')
        Publicacion.objects.create(usuario=request.user, contenido=contenido, imagen=imagen)
        return redirect('inicio')
    return render(request, 'agregar_publicacion.html')

#ME GUSTA------------------------------------------------------------------------------------------------
from django.http import JsonResponse

@login_required
def me_gusta(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id)
    if request.user in publicacion.me_gusta.all():
        publicacion.me_gusta.remove(request.user)  # Quitar el "me gusta"
        estado = 'removed'
    else:
        publicacion.me_gusta.add(request.user)  # Agregar el "me gusta"
        estado = 'added'

    return JsonResponse({'estado': estado, 'total_me_gusta': publicacion.total_me_gusta()})


#PERFIL------------------------------------------------------------------------------------------------------------------

@login_required
def perfil(request):
    # Si el usuario ya tiene un perfil, lo obtenemos
    try:
        perfil = Perfil.objects.get(usuario=request.user)
    except Perfil.DoesNotExist:
        perfil = None

    # Si el formulario ha sido enviado
    if request.method == 'POST':
        if perfil:
            form = PerfilForm(request.POST, request.FILES, instance=perfil)
        else:
            # Si no existe perfil, creamos uno nuevo y asignamos al usuario logueado
            form = PerfilForm(request.POST, request.FILES)
            if form.is_valid():
                nuevo_perfil = form.save(commit=False)
                nuevo_perfil.usuario = request.user  # Asignamos el usuario logueado
                nuevo_perfil.save()
                return redirect('perfil')  # Redirigir de nuevo al perfil

        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirigir de nuevo al perfil
    
    else:
        if perfil:
            form = PerfilForm(instance=perfil)
        else:
            form = PerfilForm()

    return render(request, 'perfil.html', {'form': form, 'perfil': perfil})
#CERRAR SESION---------------------------------------------------------------------------------------------------------

def cerrar_sesion(request):
    # Cierra la sesión del usuario
    logout(request)
    # Redirige a la página de inicio
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('inicio')  # Cambia 'inicio' por el nombre de tu URL de inicio

#AMIGOS----------------------------------------------------------------------------------------------------------------

# Ver todos los usuarios registrados
@login_required
def ver_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'ver_usuarios.html', {'usuarios': usuarios})

# Seguir a un usuario
@login_required
def seguir_usuario(request, usuario_id):
    usuario_a_seguir = User.objects.get(id=usuario_id)
    if usuario_a_seguir != request.user:  # No puedes seguirte a ti mismo
        Seguimiento.objects.get_or_create(seguidor=request.user, seguido=usuario_a_seguir)
    return redirect('ver_usuarios')

# Ver usuarios seguidos
@login_required
def ver_seguidos(request):
    seguidos = Seguimiento.objects.filter(seguidor=request.user)
    return render(request, 'ver_seguidos.html', {'seguidos': seguidos})

# Ver seguidores
@login_required
def ver_seguidores(request):
    # Obtener los seguidores del usuario actual
    seguidores = Seguimiento.objects.filter(seguido=request.user)
    return render(request, 'ver_seguidores.html', {'seguidores': seguidores})

# Ver amigos
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Amistad, Mensaje  # Asegúrate de tener los modelos correctos

@login_required
def ver_amigos(request):
    # Obtener los amigos del usuario
    amigos = Amistad.objects.filter(usuario1=request.user) | Amistad.objects.filter(usuario2=request.user)

    # Obtener el último chat entre el usuario y cualquier amigo
    ultimo_chat = Mensaje.objects.filter(
        emisor=request.user
    ).order_by('-fecha').first()  # Obtener el último mensaje enviado por el usuario

    if not ultimo_chat:
        # Si no hay chat, asignamos un valor por defecto
        ultimo_chat_id = None
    else:
        # Si hay un último chat, obtenemos el ID del receptor
        ultimo_chat_id = ultimo_chat.receptor.id if ultimo_chat.receptor != request.user else ultimo_chat.emisor.id

    return render(request, 'ver_amigos.html', {
        'amigos': amigos,
        'ultimo_chat_id': ultimo_chat_id,  # Pasamos el ID del último chat
    })

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Seguimiento)
def crear_amistad_si_es_mutua(sender, instance, created, **kwargs):
    if created:
        seguidor = instance.seguidor
        seguido = instance.seguido

        # Verificar si el seguido también sigue al seguidor
        if Seguimiento.objects.filter(seguidor=seguido, seguido=seguidor).exists():
            # Verificar si la amistad ya existe
            if not Amistad.objects.filter(usuario1=seguidor, usuario2=seguido).exists() and \
               not Amistad.objects.filter(usuario1=seguido, usuario2=seguidor).exists():
                Amistad.objects.create(usuario1=seguidor, usuario2=seguido)

from django.db.models.signals import post_delete

@receiver(post_delete, sender=Seguimiento)
def eliminar_amistad_si_es_necesario(sender, instance, **kwargs):
    seguidor = instance.seguidor
    seguido = instance.seguido

    # Si ya no hay un seguimiento mutuo, eliminar la amistad
    if not Seguimiento.objects.filter(seguidor=seguido, seguido=seguidor).exists():
        Amistad.objects.filter(usuario1=seguidor, usuario2=seguido).delete()
        Amistad.objects.filter(usuario1=seguido, usuario2=seguidor).delete()

#MENSAJES----------------------------------------------------------------------------------------------------------
@login_required
def enviar_mensaje(request, receptor_id):
    receptor = get_object_or_404(User, id=receptor_id)
    
    if request.method == 'POST':
        contenido = request.POST.get('mensaje')
        Mensaje.objects.create(emisor=request.user, receptor=receptor, contenido=contenido)
        return redirect('chat', receptor_id=receptor.id)

    return render(request, 'enviar_mensaje.html', {'receptor': receptor})
@login_required
def chat(request, receptor_id):
    receptor = get_object_or_404(User, id=receptor_id)
    mensajes = Mensaje.objects.filter(
        (Q(emisor=request.user) & Q(receptor=receptor)) |
        (Q(emisor=receptor) & Q(receptor=request.user))
    ).order_by('fecha')

    # Marcar mensajes como leídos
    mensajes.filter(receptor=request.user, leido=False).update(leido=True)

    if request.method == 'POST':
        contenido = request.POST.get('mensaje')
        if contenido:  # Verificar que el contenido no esté vacío
            Mensaje.objects.create(emisor=request.user, receptor=receptor, contenido=contenido)
            return redirect('chat', receptor_id=receptor.id)  # Redirigir al mismo chat para ver el nuevo mensaje

    return render(request, 'chat.html', {'receptor': receptor, 'mensajes': mensajes})

from django.db.models import Count

@login_required
def bandeja_entrada(request):
    # Obtener los mensajes no leídos agrupados por emisor
    mensajes_no_leidos = Mensaje.objects.filter(receptor=request.user, leido=False) \
        .values('emisor') \
        .annotate(cantidad=Count('id')) \
        .order_by('cantidad')  # Puedes cambiar el orden según lo que necesites

    # Obtener los usuarios que han enviado los mensajes
    emisores = []
    for mensaje in mensajes_no_leidos:
        emisor = User.objects.get(id=mensaje['emisor'])  # Obtenemos el objeto User a partir del id
        emisores.append({
            'emisor': emisor,
            'cantidad': mensaje['cantidad']
        })

    return render(request, 'bandeja_entrada.html', {'emisores': emisores})

#AGREGAR HISTORIA-------------------------------------------------------------------------------------------------------
# Vista para ver las historias
def ver_historias(request):
    historias = Historia.objects.all()

    # Añadir conteos de reacciones al contexto
    historias_con_reacciones = []
    for historia in historias:
        likes = Reaccion.objects.filter(historia=historia, tipo_reaccion='like').count()
        dislikes = Reaccion.objects.filter(historia=historia, tipo_reaccion='dislike').count()
        historias_con_reacciones.append({
            'historia': historia,
            'likes': likes,
            'dislikes': dislikes,
        })

    return render(request, 'ver_historias.html', {'historias_con_reacciones': historias_con_reacciones})

# Vista para agregar una historia
@login_required
def agregar_historia(request):
    if request.method == 'POST':
        form = HistoriaForm(request.POST, request.FILES)
        if form.is_valid():
            historia = form.save(commit=False)
            historia.usuario = request.user
            historia.fecha_publicacion = timezone.now()
            historia.save()
            return redirect('ver_historias')  # Redirigir a la página de historias
    else:
        form = HistoriaForm()

    return render(request, 'agregar_historia.html', {'form': form})


# Vista para reaccionar a una historia
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def reaccionar_historia(request, historia_id, reaccion):
    historia = get_object_or_404(Historia, id=historia_id)

    if reaccion not in ['like', 'dislike']:
        return JsonResponse({'error': 'Reacción no válida'}, status=400)

    reaccion_existente = Reaccion.objects.filter(historia=historia, usuario=request.user).first()

    if reaccion_existente:
        reaccion_existente.tipo_reaccion = reaccion
        reaccion_existente.save()
    else:
        Reaccion.objects.create(historia=historia, usuario=request.user, tipo_reaccion=reaccion)

    # Contar las reacciones actualizadas
    likes = Reaccion.objects.filter(historia=historia, tipo_reaccion='like').count()
    dislikes = Reaccion.objects.filter(historia=historia, tipo_reaccion='dislike').count()

    return JsonResponse({'likes': likes, 'dislikes': dislikes})
