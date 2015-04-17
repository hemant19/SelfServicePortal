from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'SelfServicePortal.views.index', name='Index'),
    url(r'^register/$', 'signups.views.register', name='Register'),
    url(r'^login/$', 'signups.views.login_view', name='Login'),
    url(r'^logout/$', 'signups.views.logout_view', name='Logout'),
    url(r'^thankyou/$', 'signups.views.thankyou', name='Thank You'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
