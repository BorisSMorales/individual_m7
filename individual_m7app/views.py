from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .models import Task



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
        tasks = Task.objects.filter(user=request.user, status='pendiente').order_by('due_date')

        return render(request, 'lista_tareas.html', {'tasks': tasks})

