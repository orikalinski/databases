from django.conf.urls import patterns, include, url
from views import index, filter_places_by_opening_hours_and_rating, \
    filter_places_by_address_and_rating, filter_by_all_params

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gmp_databases.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', index),
    url('^filter_oh_and_rating/(\d)/(\d{2,2}\:\d{2,2})/(\d{2,2}\:\d{2,2})/(\d\.\d)/',
        filter_places_by_opening_hours_and_rating),
    url('^filter_address_and_type/(.+)/(\d{1,5})/(\d\.\d)/',
        filter_places_by_address_and_rating),
    url('^filter_by_all_params/(\d)/(\d{2,2}\:\d{2,2})/(\d{2,2}\:\d{2,2})/(.+)/(\d{1,5})/(\d\.\d)/(.+)/',
        filter_by_all_params)
)
