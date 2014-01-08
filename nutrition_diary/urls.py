from __future__ import absolute_import, division, unicode_literals
from django.conf.urls import patterns, include, url
from app import views, forms

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'nutrition_diary.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.index, name='index'),
                       url(r'^add/(?P<url>.+)', views.scrape, name='add'),
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'login.html', 'authentication_form': forms.LoginForm},'login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'next_page': '/'}, name='logout'),
                       url(r'^food_types/$', views.food_types, name='food_types'),
                       url(r'^food_type/(?P<id>\d+)/$', views.food_type, name='food_type'),
                       url(r'^food_type/(?P<id>\d+)/serving/$', views.edit_ft_serving,
                           name='edit_ft_serving'),
                       url(r'^diary/$', views.diary, name='diary'),
                       url(r'^serving/(?P<id>\d+)/$', views.delete_serving, name='serving')
)
