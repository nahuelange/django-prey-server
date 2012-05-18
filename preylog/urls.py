from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'preyserver.views.home', name='home'),
    # url(r'^preyserver/', include('preyserver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^devices.xml$', 'preylog.views.devices'),
    url(r'^devices/(?P<key>.*).xml$', 'preylog.views.device'),
    url(r'^report/(?P<key>.*).xml$', 'preylog.views.report'),
    url(r'^', 'preylog.views.log'),
)
