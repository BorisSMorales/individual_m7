from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Task
from django.http import JsonResponse



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
    def get(self, request):
        # Obtener todas las tareas pendientes del usuario actual, ordenadas por fecha de vencimiento
        tasks = Task.objects.filter(user=request.user.id, estado='pendiente').order_by('fecha_limite')

        return render(request, 'lista_tareas.html', {'tasks': tasks})
    
class TareaDetalleView(View):

    def get(self, request, tarea_id):
        # Obtener la tarea específica o mostrar un error 404 si no existe
        tarea = get_object_or_404(Task, id=tarea_id)

        return render(request, 'detalle_tarea.html', {'tarea': tarea})
    
def confirmar_eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Task, id=tarea_id)
    return render(request, 'confirmar_eliminar_tarea.html', {'tarea': tarea})

def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Task, id=tarea_id)
    tarea.delete()
    return redirect('Tareaslista')

