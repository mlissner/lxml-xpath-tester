from django.conf.urls.defaults import patterns

from tester.views import run_xpath

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xpathtester.views.home', name='home'),
    # url(r'^xpathtester/', include('xpathtester.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', run_xpath),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '',
         'show_indexes': True}),
)
