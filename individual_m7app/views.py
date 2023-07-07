from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Task, Etiqueta
from django.http import JsonResponse
from .forms import CrearTareaForm, ObservacionForm
from django.urls import reverse_lazy

from individual_m7app.forms import LoginForm

# Create your views here.

def landing(request):
    return render(request, 'landingpage.html')

class Ingreso(TemplateView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, { "form": form })

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('landing')
            form.add_error('username', 'Credenciales incorrectas')
            return render(request, self.template_name, { "form": form })
        else:
            return render(request, self.template_name, { "form": form })
        



class TareasListaView(View):

    etiquetas_disponibles = Etiqueta.objects.all()
    def get(self, request):
        # Obtener todas las tareas pendientes del usuario actual
        tasks = Task.objects.filter(user=request.user, estado='pendiente')

        # Obtener los valores únicos para las etiquetas y pasarlos al formulario
        etiquetas = Task.objects.filter(user=request.user).values_list('etiqueta__name', flat=True).distinct()

        # Obtener los valores únicos para las fechas límite y pasarlos al formulario
        fechas_limite = Task.objects.filter(user=request.user).values_list('fecha_limite', flat=True).distinct()

        # Obtener otros valores únicos para los campos de filtrado (si es necesario)

        # Procesar el formulario de filtrado
        etiqueta_filtro = request.GET.get('etiqueta')
        fecha_limite_filtro = request.GET.get('fecha_limite')

        if etiqueta_filtro:
            tasks = tasks.filter(etiqueta__name=etiqueta_filtro)

        if fecha_limite_filtro:
            tasks = tasks.filter(fecha_limite=fecha_limite_filtro)

        # Pasar los valores de filtrado al contexto para mostrarlos en el formulario
        contexto = {
            'tasks': tasks,
            'etiquetas': etiquetas,
            'fechas_limite': fechas_limite,
            'etiqueta_filtro': etiqueta_filtro,
            'fecha_limite_filtro': fecha_limite_filtro
        }
        return render(request, 'lista_tareas.html', {'tasks': tasks, 'etiquetas': etiquetas}) 
       
class TareaDetalleView(View):
    template_name = 'detalle_tarea.html'
    form_class = ObservacionForm

    def get(self, request, task_id):
        tarea = get_object_or_404(Task, id=task_id)
        observaciones_anteriores = tarea.observacion if tarea.observacion else ''
        form = self.form_class(initial={'observaciones': observaciones_anteriores})

        context = {
            'tarea': tarea,
            'form': form,
            'prioridad': tarea.prioridad,  # Agrega el campo prioridad al contexto
        }

        return render(request, self.template_name, context)
    
    def post(self, request, task_id):
        tarea = get_object_or_404(Task, id=task_id)
        form = ObservacionForm(request.POST)
        if form.is_valid():
            observaciones = form.cleaned_data['observaciones']
            tarea.observacion = observaciones
            tarea.save()
        return redirect('Tareaslista')
    
def confirmar_eliminar_tarea(request, task_id):
    tarea = get_object_or_404(Task, id=task_id)
    return render(request, 'confirmar_eliminar_tarea.html', {'tarea': tarea})

def eliminar_tarea(request, task_id):
    tarea = get_object_or_404(Task, id=task_id)
    tarea.delete()
    return redirect('Tareaslista')

def confirmar_completar_tarea(request, task_id):
    tarea = get_object_or_404(Task, id=task_id)
    return render(request, 'confirmar_completar_tarea.html', {'tarea': tarea})

def completar_tarea(request, task_id):
    tarea = get_object_or_404(Task, id=task_id)
    tarea.estado = 'completada'
    tarea.save()
    return redirect('Tareaslista')

class CrearTareaView(View):
    template_name = 'crear_tarea.html'
    form_class = CrearTareaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            if request.user.is_staff:  # Verifica si el usuario es "staff"
                tarea.user = form.cleaned_data['usuario']  # Asigna el usuario seleccionado en el formulario
            else:
                tarea.user = request.user  # Asigna el usuario actual
            etiqueta_id = form.cleaned_data['etiqueta']  # Obtén el ID de la etiqueta seleccionada
            etiqueta = Etiqueta.objects.get(id=etiqueta_id)  # Recupera la instancia de la etiqueta
            tarea.etiqueta = etiqueta  # Asigna la etiqueta a la tarea
            tarea.save()
            return redirect('Tareaslista')
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form.fields['etiqueta'].queryset = Etiqueta.objects.all()  # Agrega el queryset de etiquetas al formulario
        return render(request, self.template_name, {'form': form})
    
class EditarTareaView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        form = CrearTareaForm(instance=task)
        return render(request, 'tarea_editar.html', {'form': form})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        form = CrearTareaForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('Tareaslista')
        return render(request, 'tarea_editar.html', {'form': form})
    
class TareasHistorialView(View):
    def get(self, request):
        # Obtener todas las tareas
        tasks = Task.objects.all()

        return render(request, 'historial_tareas.html', {'tasks': tasks})
    
    