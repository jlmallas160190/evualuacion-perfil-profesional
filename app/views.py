#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User,Group
from django import forms
from django.core.context_processors import csrf
from django.contrib import auth
from django.shortcuts import redirect
from django.forms.forms import NON_FIELD_ERRORS
from django.utils import simplejson
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password

from app.models import Cuestionario
from app.models import Estudiante
from app.models import Pregunta
from app.models import Item_Pregunta
from app.models import Usuario
from app.models import Estudiante
from app.models import Seccion
from app.models import Test
from app.models import Contestacion
from app.models import Periodo_Test
from app.models import Periodo_Actual
# Create your views here.									
											  
def login(request):
    form = forms.Form()
    form.fields['username'] = forms.CharField(label="Cedula", max_length=30, 
                                              widget=forms.TextInput(attrs={'title': 'Cedula',}),
                                              error_messages={'required':'Ingrese nombre de usuario'})


    form.fields['password'] = forms.CharField(label="Clave SGA", 
                                              widget=forms.PasswordInput(attrs={'title': 'Clave Cedula',}),
                                              error_messages={'required':'Ingrese el password'})
    data = dict(form=form)
	  
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
		
        user = auth.authenticate(username=username,password=password)
		#user = Usuario.objects.get(username=username, password=password)	
        if user is not None and user.is_active:
            auth.login(request, user)
            if  user.groups.filter(id=1): 
                return HttpResponseRedirect('inicio')
            else:
				if  user.is_superuser:
					#return HttpResponseRedirect('/usuarios/generar')
					return redirect('/logout')
				else:
					return redirect('/logout')
        else:
            form.full_clean()
            form._errors[NON_FIELD_ERRORS] = form.error_class(['Error de usuario o contraseña'])
    data.update(csrf(request))
    return render_to_response("app/login.html",data)
	
@login_required()
def generar_usuarios(request):
	datos = dict()
	if(request.user.is_superuser):
		datos.update(dict(user=request.user))
		return render_to_response("app/generar_usuarios.html",datos,RequestContext(request))
	else:
		return redirect('/logout')
	
def grabar_usuarios(request):
	estudiantes=Estudiante.objects.all()
	datos = dict()
	for estudiante in estudiantes:
		if(estudiante.usuarios.all() is None):
			user=User(username=estudiante.numero_identificacion,last_login=datetime.now().date(),is_superuser=0, is_active=1,is_staff=0,first_name=estudiante.nombres,last_name=estudiante.apellidos)
			user.password=make_password(estudiante.numero_identificacion)
			user.save()
			usuario=Usuario(user=user, estudiante=estudiante)
			usuario.save()
	return render_to_response("app/usuarios_guardados.html", {'mensaje':'Usuarios grabados satisfactoriamente'},context_instance=RequestContext(request))
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required()
def inicio(request):
	cuestionarios=[]
	datos = dict()
	periodoActual=Periodo_Actual.getPeriodoTestActual()
	periodo_finalizado = False
	periodo_no_iniciado = False
	if periodoActual.noIniciado():
		periodo_no_iniciado = True
	elif periodoActual.vigente():
		cuestionarios=Cuestionario.objects.all()
	elif periodoActual.finalizado():
		periodo_finalizado=True
	usuario= Usuario.objects.get(user_id=request.user.id)
	estudiante=usuario.estudiante
	request.session['estudiante']=estudiante
	datos.update(dict(usuario=usuario,cuestionarios=cuestionarios, periodo_no_iniciado=periodo_no_iniciado, periodo_finalizado=periodo_finalizado))
	return render_to_response("app/index.html",datos,
        RequestContext(request))
def test_responder(request, id_cuestionario):
	datos = dict()
	test = Test()
	cuestionario_estudiante_contestado=None
	cuestionario = Cuestionario.objects.get(id=id_cuestionario)
	estudiante=request.session.get('estudiante', None)
	# for test in estudiante.tests.all():
		# if test.cuestionario == cuestionario:
			# cuestionario_estudiante_contestado=test.cuestionario
	# if cuestionario_estudiante_contestado != None :
		# return  render_to_response('app/test_finalizado.html', {'mensaje':'Ud. ya contesto este Test'}, context_instance=RequestContext(request))
	# else:
	fecha = datetime.now()
	usuario= Usuario.objects.get(user_id=request.user.id)
	estudiante= Estudiante.objects.get(id=usuario.estudiante_id)
	test.fecha= datetime.now().date()
	test.nombre=cuestionario.nombre
	test.hora_inicio = datetime.now().time()
	test.cuestionario = cuestionario
	test.estudiante=estudiante
	request.session['test'] = test
	datos.update(dict(cuestionario=cuestionario,fecha=fecha, estudiante=estudiante,usuario=usuario))
	return render_to_response("app/test.html", datos, context_instance=RequestContext(request))
def test_grabar(request):
	test = request.session.get('test', None)
	cuestionario_estudiante_contestado=None
	estudiante=request.session.get('estudiante', None)
	# for testContestado in estudiante.tests.all():
		# if testContestado.cuestionario == test.cuestionario:
			# cuestionario_estudiante_contestado=testContestado.cuestionario
	# if cuestionario_estudiante_contestado != None:
		# return  render_to_response('app/test_finalizado.html', {'mensaje':'Ud. ya contesto este Test'}, context_instance=RequestContext(request))
	# else:
	test.hora_fin = datetime.now().time()
	test.save()
	for v,k in request.POST.items():
		if k.startswith('csrf'):
			continue
		if k.startswith('pregunta'):
			id_pregunta = int(k.split('-')[1])
			contestacion = Contestacion(pregunta_id=id_pregunta, respuesta_id=v, test=test)
			contestacion.save()
	return  render_to_response('app/test_finalizado.html', {'mensaje':'Test grabado satisfactoriamente'}, context_instance=RequestContext(request))