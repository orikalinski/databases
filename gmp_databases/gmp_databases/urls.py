from django.conf.urls import patterns, include, url
from views import home_page_stats, filter_places_by_opening_hours_and_type, \
    filter_places_by_address_and_rating, filter_by_all_params, get_place_details, \
    get_place_images, insert_image, insert_review, get_complicated_stats, text_search, \
    redirect_to_homepage


from django.contrib import admin
admin.autodiscover()

urlpatterns = [url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', home_page_stats),
    url('^$', redirect_to_homepage),
    url('^opening_hours_and_type_search/', filter_places_by_opening_hours_and_type),
    url('^address_and_rating_search/', filter_places_by_address_and_rating),
    url('^full_search/', filter_by_all_params),
    url('^place/', get_place_details),
    url('^gallery/', get_place_images),
    url('^uploads/', insert_image),
    url('^insert_review/', insert_review),
    url('^statistics/', get_complicated_stats),
    url('^text_search/', text_search)]
