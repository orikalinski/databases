from django.conf.urls import patterns, include, url
from views import home_page_stats, filter_places_by_opening_hours_and_type, \
    filter_places_by_address_and_rating, filter_by_all_params

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gmp_databases.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', home_page_stats),
    url('^opening_hours_and_type_search/',
        filter_places_by_opening_hours_and_type),
    url('^address_and_rating_search/',
        filter_places_by_address_and_rating),
    url('^full_search/',
        filter_by_all_params)
)
