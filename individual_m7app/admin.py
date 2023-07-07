from django.contrib import admin
from .models import Etiqueta
from .models import Prioridad

# Register your models here.

@admin.register(Etiqueta)
class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Prioridad)

