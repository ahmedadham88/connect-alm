from django.conf.urls import include, url
from django.contrib import admin
from ConnectAlmMainApp import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'connectAlm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^connect/(?P<input>\w{0,50})/$', views.connect),
    url(r'^follow/(?P<input>\w{0,50})/$',views.follow),
    url(r'^poll/(?P<sig>\w{0,50})/$', views.poll),
    url(r'^unfollow/(?P<input>\w{0,50})/$',views.unfollow),

]
