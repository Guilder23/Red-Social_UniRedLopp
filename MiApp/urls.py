
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página principal
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('logout/', views.cerrar_sesion, name='logout'),  # Ruta personalizada para cerrar sesión
    path('agregar_publicacion/', views.agregar_publicacion, name='agregar_publicacion'),
    path('comentar/<int:publicacion_id>/', views.comentar, name='comentar'),
    path('me_gusta/<int:publicacion_id>/', views.me_gusta, name='me_gusta'),
    path('perfil/', views.perfil, name='perfil'),
    path('ver_usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('seguir/<int:usuario_id>/', views.seguir_usuario, name='seguir_usuario'),
    path('seguidores/', views.ver_seguidores, name='ver_seguidores'),
    path('seguidos/', views.ver_seguidos, name='ver_seguidos'),
    path('amigos/', views.ver_amigos, name='ver_amigos'),
    path('enviar/<int:receptor_id>/', views.enviar_mensaje, name='enviar_mensaje'),
    path('chat/<int:receptor_id>/', views.chat, name='chat'),
    path('bandeja/', views.bandeja_entrada, name='bandeja_entrada'),
    path('historias/', views.ver_historias, name='ver_historias'),
    path('agregar_historia/', views.agregar_historia, name='agregar_historia'),
    path('reaccionar/<int:historia_id>/<str:reaccion>/', views.reaccionar_historia, name='reaccionar_historia'),
]


