from django.contrib import admin
from app.models import Perfil, Caracteristica, Caracteristica_Perfil,Catalogo_Caracteristica,Pregunta,Item_Pregunta,Cuestionario,Seccion,Tipo_Pregunta,Usuario
from app.models import Periodo_Test
from app.models import Periodo_Actual
from app.models import Contestacion
from app.models import Test
from django.contrib.auth.models import User
admin.site.register(Perfil)
admin.site.register(Catalogo_Caracteristica)
admin.site.register(Caracteristica)
admin.site.register(Caracteristica_Perfil)
admin.site.register(Pregunta)
admin.site.register(Item_Pregunta)
admin.site.register(Cuestionario)
admin.site.register(Seccion)
admin.site.register(Tipo_Pregunta)
admin.site.register(Periodo_Test)
admin.site.register(Periodo_Actual)

class TestAdmin(admin.ModelAdmin):
	readonly_fields = ('nombre','fecha','hora_inicio','hora_fin','estudiante','cuestionario')
	list_display = ('estudiante','nombre','fecha','hora_inicio','hora_fin')
	list_filter = ['estudiante']
	list_per_page = 25
admin.site.register(Test,TestAdmin)
class ContestacionAdmin(admin.ModelAdmin):
	readonly_fields = ('test','respuesta','pregunta')
	list_display = ('estudiante','test','fecha_test')
	list_filter = ['respuesta']
	list_per_page = 10
	search_fields = ['pregunta.texto', 'respuesta.nombre']
#admin.site.register(Contestacion,ContestacionAdmin)
# Register your models here.
