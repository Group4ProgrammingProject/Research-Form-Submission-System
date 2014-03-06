

from django.contrib import admin
 #admin.autodiscover();
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:



urlpatterns = patterns('',

    url(r'^$', 'users.views.dashboard', name='dashboard'),
	url(r'^login/', 'users.views.login', name='login'),
    url(r'^logout/', 'users.views.logout', name='logout'),
    url(r'^create_user/', 'users.views.create_user', name='create_user'),
    url(r'^create_key/', 'users.views.create_key', name='create_key'),
    url(r'^invite/', 'users.views.invite', name='invite'),
    url(r'^accept_invite/', 'users.views.accept_invite', name='accept_invite'),
	url(r'^accounts/', include('email_registration.urls')),



    # Examples:
    # url(r'^$', 'ReviewSubmission.views.home', name='home'),
    # url(r'^ReviewSubmission/', include('ReviewSubmission.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)