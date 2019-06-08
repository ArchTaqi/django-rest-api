from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import generic


from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Django Pet Store APIs Docs')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs1/', include_docs_urls(title='APIs Docs', public=False)),
    path('docs/', schema_view),
    path('robots.txt', TemplateView.as_view(template_name='DjangoRestApi/robots.txt', content_type="text/plain")),
    ]

urlpatterns += [
    path('', generic.TemplateView.as_view(template_name='index.html'), name="index"),
    path('', include('apps.users.urls')),
    path('', include('apps.pets.urls')),

    # re_path('api/(?P<version>(v1|v2))/', include('apps.music.urls'))
    # path(r'^api/v1/', include(apipatterns, namespace='api')),

    # path(r'^simpleemail/(?P<emailto>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/',
    #      sendSimpleEmail,
    #      name='sendSimpleEmail'
    #      ),
    # path(
    #     r'^massEmail/(?P<emailto1>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<emailto2>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})',
    #     sendMassEmail,
    #     name='sendMassEmail'
    #     ),
    # path(r'^htmlemail/(?P<emailto>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/',
    #      sendHTMLEmail,
    #      name='sendHTMLEmail'
    #      ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    re_path('^media/(?P<path>.*)', serve,
            {'document_root': settings.MEDIA_ROOT})
]