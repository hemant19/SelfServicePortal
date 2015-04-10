from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'SelfServicePortal.views.Index', name='Index'),
    url(r'^register/$', 'signups.views.Register', name='Register'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
