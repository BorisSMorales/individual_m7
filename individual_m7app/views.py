from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect



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

