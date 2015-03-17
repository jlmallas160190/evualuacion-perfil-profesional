#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Estudiante(models.Model):
	id = models.AutoField(primary_key=True)
	genero= models.CharField(max_length=50)
	nombres = models.CharField(max_length=250)
	apellidos = models.CharField(max_length=250)
	fecha_nacimiento = models.DateField()
	numero_identificacion=models.CharField(max_length=50)
	email=models.EmailField();
	telefono = models.CharField(max_length=50)
	celular = models.CharField(max_length=50)
	direccion = models.CharField(max_length=250)
	pais = models.CharField(max_length=250)
	provincia = models.CharField(max_length=250)
	def __unicode__(self):
		return self.nombres +" "+self.apellidos
class Perfil(models.Model):
	id = models.AutoField(primary_key=True)
	nombre =models.CharField(max_length=250)
	sigla =models.CharField(max_length=2500)
	descripcion=models.TextField(max_length=250)
	def __unicode__(self):
		return self.nombre
class Catalogo_Caracteristica(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=250)
	def __unicode__(self):
		return self.nombre
class Caracteristica(models.Model):
	id = models.AutoField(primary_key=True)
	catalogo_caracteristica_fk= models.ForeignKey(Catalogo_Caracteristica,verbose_name="Tipo")
	nombre = models.TextField(max_length=250)
	def __unicode__(self):
		return self.nombre+"-"+self.catalogo_caracteristica_fk.nombre
class Caracteristica_Perfil(models.Model):
	id = models.AutoField(primary_key=True)
	perfil_id_fk= models.ForeignKey(Perfil,verbose_name="Perfil")
	caracteristica_id_fk= models.ForeignKey(Caracteristica,verbose_name="Caractesristica")
	def __unicode__(self):
		return "Perfil: "+ self.perfil_id_fk.nombre+" Caracteristica: "+self.caracteristica_id_fk.nombre
class Periodo_Test(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=250)
	descripcion=models.TextField(max_length=500)
	fecha_inicio=models.DateTimeField()
	fecha_fin=models.DateTimeField()
	class Meta:
		ordering = ['fecha_inicio', 'fecha_fin']
		verbose_name = u'Periodo Test'
	   
	def noIniciado(self):
		ahora = datetime.today()
		return ahora < self.fecha_inicio
    
	def vigente(self):
		ahora = datetime.today()
		return self.fecha_inicio <=  ahora <= self.fecha_fin 

	def finalizado(self):
		ahora = datetime.today()
		return ahora > self.fecha_fin
	def __unicode__(self):
		return self.nombre
class Periodo_Actual(models.Model):
	id = models.AutoField(primary_key=True)
	periodo_test=models.ForeignKey(Periodo_Test,verbose_name="Periodo")
	@classmethod
	def getPeriodoTestActual(self):
		return Periodo_Actual.objects.get(id=1).periodo_test
	def __unicode__(self):
		return self.periodo_test.nombre	
class Cuestionario(models.Model):
	id = models.AutoField(primary_key=True)
	titulo = models.CharField(max_length=250)
	nombre = models.CharField(max_length=250)
	periodo_test=models.ForeignKey(Periodo_Test,verbose_name="Periodo")
	def __unicode__(self):
		return self.nombre		
class Test(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=250)
	fecha=models.DateField();
	hora_inicio=models.TimeField()
	hora_fin=models.TimeField()
	estudiante=models.ForeignKey(Estudiante, related_name='tests',null=True, blank=True)
	cuestionario=models.ForeignKey(Cuestionario,verbose_name="Cuestionario")
	
	def __unicode__(self):
		return self.nombre
class Tipo_Pregunta(models.Model):	
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=250)
	descripcion = models.CharField(max_length=250)
	def __unicode__(self):
		return self.nombre
class Seccion(models.Model):
	id = models.AutoField(primary_key=True)
	titulo = models.CharField(max_length=250)
	descripcion = models.CharField(max_length=250)
	cuestionario=models.ForeignKey(Cuestionario, related_name='secciones',null=True, blank=True)
	
	def __unicode__(self):
		return self.titulo
		
class Pregunta(models.Model):
	id = models.AutoField(primary_key=True)
	texto = models.CharField(max_length=250)
	orden=models.IntegerField(max_length=11)
	tipo_pregunta_id_fk=models.ForeignKey(Tipo_Pregunta,verbose_name="Tipo")
	seccion=models.ForeignKey(Seccion,related_name='preguntas',null=True, blank=True)
	def __unicode__(self):
		return self.texto
class Item_Pregunta(models.Model):
	id = models.AutoField(primary_key=True)
	caracteristica=models.ForeignKey(Caracteristica, verbose_name="Caracteristica")
	texto=models.CharField(max_length=250)
	pregunta=models.ForeignKey(Pregunta,related_name='items',null=True, blank=True)
	def __unicode__(self):
		return self.caracteristica.nombre
class Contestacion(models.Model):	
	id = models.AutoField(primary_key=True)
	pregunta=models.ForeignKey(Pregunta,verbose_name="Pregunta")
	respuesta=models.ForeignKey(Caracteristica,verbose_name="Respuesta")
	test=models.ForeignKey(Test,verbose_name="Test")
	def estudiante(self):
		return self.test.estudiante
	def fecha_test(self):
		return self.test.fecha
class Usuario(models.Model):
	id = models.AutoField(primary_key=True)
	user=models.ForeignKey(User,verbose_name="User")
	estudiante=models.ForeignKey(Estudiante,related_name='usuarios',null=True, blank=True)
	