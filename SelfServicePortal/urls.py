from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'SelfServicePortal.views.index', name='Index'),
    url(r'^register/$', 'signups.views.register', name='Register'),
    url(r'^login/$', 'signups.views.login_view', name='Login'),
    url(r'^logout/$', 'signups.views.logout_view', name='Logout'),
    url(r'^thankyou/$', 'signups.views.thankyou', name='Thank You'),
    url(r'^createvm/$', 'userdash.views.createInstanceView', name='Create Instances'),
    url(r'^viewvms/$', 'userdash.views.viewInstance', name='View Instances'),
    url(r'^usage/$', 'userdash.views.usageHistory', name='Usage History'),
    url(r'^terminate/$', 'userdash.views.terminateInstanceView', name='terminate instance'),
    url(r'^start/$', 'userdash.views.startInstanceView', name='start instance'),
    url(r'^stop/$', 'userdash.views.stopInstanceView', name='stop instance'),
    url(r'^vnc/$', 'userdash.views.viewConsole', name='vnc console'),

    url(r'^admin/', include(admin.site.urls)),
]
