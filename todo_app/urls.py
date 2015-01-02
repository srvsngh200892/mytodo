from django.conf.urls import patterns, include, url
from todo.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'todo_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'todo.views.auth_login', name='user_login'),
    url(r'^logout/$', 'todo.views.user_logout', name='user_logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
    url(r'^home/add/task/$', 'todo.views.add_task',name='add_task'),
    url(r'^home/edit/task/(?P<tid>[a-zA-Z0-9]+)/$', 'todo.views.edit_task',name='edit_task'),
)



 
