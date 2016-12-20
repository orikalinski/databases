import googlemaps
from googleplaces import GooglePlaces, types

api_key = "AIzaSyC5b1etMPL7i8z8RJ8YP_eexpOQxSO1rpw"

relevant_types = [types.TYPE_FOOD, types.TYPE_ZOO, types.TYPE_BAR,
                  types.TYPE_AQUARIUM, types.TYPE_ART_GALLERY,
                  types.TYPE_AMUSEMENT_PARK, types.TYPE_CAFE,
                  types.TYPE_SHOPPING_MALL]
set_of_fields_to_select = {"name", "website", "formatted_address", "geo_location",
                           "international_phone_number", "opening_hours",
                           "reviews", "rating"}

google_places = GooglePlaces(api_key)

print 'Finished to get addresses'
lat_lng_list = [(34.052235, -118.243683), (40.748817, -73.985428),
                (41.881832, -87.623177), (29.761993, -95.366302),
                (39.952583, -75.165222)]
results_to_persist = dict()
for start_lat, start_lng in lat_lng_list:
    for i in xrange(1):
        for j in xrange(1):
            print "Processing i: %s, j: %s" % (i, j)
            query_result = google_places.nearby_search(lat_lng={"lat": start_lat + i * 0.01,
                                                                "lng": start_lng + j * 0.01},
                                                       types=relevant_types,
                                                       radius=700)
            for place in query_result.places:
                if place.place_id in results_to_persist:
                    continue
                place.get_details()
                results_to_persist[place.place_id] = {key: value for key, value
                                                      in place.details.iteritems()
                                                      if key in set_of_fields_to_select}
                photos_urls = list()
                for photo in place.photos:
                    if hasattr(photo, "url"):
                        photos_urls.append(photo.url)
                results_to_persist[place.place_id]["photos_urls"] = photos_urls

print results_to_persist