"""
URL configuration for individual_m7 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from individual_m7app import views
from individual_m7app.views import landing ,Ingreso, TareasListaView, TareaDetalleView, CrearTareaView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('login/',Ingreso.as_view(), name='Login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tareas_lista/', TareasListaView.as_view(), name='Tareaslista'),
    path('tareas/<int:tarea_id>/', TareaDetalleView.as_view(), name='detalle_tarea'),
    path('tareas/<int:tarea_id>/eliminar/', views.confirmar_eliminar_tarea, name='confirmar_eliminar_tarea'),
    path('tareas/<int:tarea_id>/eliminar/confirmar/', views.eliminar_tarea, name='eliminar_tarea'),
    path('crear-tarea/', CrearTareaView.as_view(), name='crear_tarea'),
]
