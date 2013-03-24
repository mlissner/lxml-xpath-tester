from django.conf.urls.defaults import patterns

from django.conf import settings
from tester.views import run_xpath

urlpatterns = patterns('',
    (r'^$', run_xpath),
)

if settings.DEBUG:
    urlpatterns += patterns(
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '', 'show_indexes': True}),
    )
