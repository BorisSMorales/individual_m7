from django.contrib import admin
from .models import Etiqueta

# Register your models here.

@admin.register(Etiqueta)
class TagAdmin(admin.ModelAdmin):
    pass

