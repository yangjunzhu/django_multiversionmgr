from django.conf.urls import patterns, include, url
#import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('multiversion.views',
    url(r'^hello/', 'hello'),
    url(r'^createversion/', 'createversion'),
)
