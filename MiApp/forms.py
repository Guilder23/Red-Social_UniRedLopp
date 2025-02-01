from django import forms
from .models import Publicacion, Comentario
from .models import Perfil


from .models import Historia

# Formulario para agregar una nueva publicación
class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['contenido', 'imagen']

# Formulario para agregar un comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['bio', 'foto_perfil']


#Agregar historias
class HistoriaForm(forms.ModelForm):
    class Meta:
        model = Historia
        fields = ['contenido', 'imagen']
