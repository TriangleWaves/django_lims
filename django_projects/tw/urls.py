from django.conf.urls.defaults import patterns,include
from settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from tw import lims

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tw/', include('tw.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    (r'^lims/ipsc/report/$', 'tw.lims.admin_views.report'),
    (r'^admin/patient/report/','tw.lims.admin_views.report'),
    (r'^admin/patient/flowcell/','tw.lims.admin_views.flowcell'),
    (r'^admin/patient/ipsc/','tw.lims.admin_views.test'),
    ('', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),
#    (r'^admin/patient/report/','lims.admin_views.report'),
#    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': ROOT_PATH + '/media'}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT,'show_indexes': True}),
)
