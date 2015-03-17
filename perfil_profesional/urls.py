from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'perfil_profesional.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'app.views.login'),
	url(r'^inicio/$', 'app.views.inicio', name='index'),
	url(r'^logout/$', 'app.views.logout', name='logout'),
	#url(r'^usuarios/generar/$', 'app.views.generar_usuarios', name='generar_usuarios'),
	#url(r'^usuarios/grabar/$', 'app.views.grabar_usuarios', name='grabar_usuarios'),
	url(r'^test/responder/(\d{1,5})/$', 'app.views.test_responder',name='encuesta_responder'),
	url(r'^test/grabar/$', 'app.views.test_grabar',name='test_grabar'),
)
