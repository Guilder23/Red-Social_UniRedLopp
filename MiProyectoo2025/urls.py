

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from MiApp import views  # Asegúrate de que el import es correcto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MiApp.urls')),  # Incluye las rutas de MiApp
]

# Manejo de archivos estáticos y medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

