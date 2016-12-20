from bs4 import BeautifulSoup
from datetime import datetime, time
from itertools import cycle
import os
from googleplaces import GooglePlaces, types, GooglePlacesError

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "gmp_databases.gmp_databases.settings")

from gmp_databases.gmp_databases.models import User, Place, \
    Image, Country, City, Type, Location, LOCATION_TYPE, OpeningHours

api_keys = ["AIzaSyC5b1etMPL7i8z8RJ8YP_eexpOQxSO1rpw",
            "AIzaSyAu4PKwcADVNSbjkfs6wOcxNeEHtHO6boQ",
            "AIzaSyDzg62HDHaGRXK1OiRB39eACDG6CNFn",
            "AIzaSyD9asahayiUzfBCYv4GjKyoROpjwUraDgU"]

relevant_types = [types.TYPE_FOOD, types.TYPE_ZOO, types.TYPE_BAR,
                  types.TYPE_AQUARIUM, types.TYPE_ART_GALLERY,
                  types.TYPE_AMUSEMENT_PARK, types.TYPE_CAFE,
                  types.TYPE_SHOPPING_MALL]
set_of_fields_to_select = {"name", "website", "formatted_address", "geometry",
                           "international_phone_number", "opening_hours",
                           "reviews", "rating", "adr_address", "types"}

api_key_cool_down = 3600
deactivated_keys = list()

active_google_places_list = [(i, GooglePlaces(api_key))
                             for i, api_key in enumerate(api_keys)]
active_google_places_cycle = cycle(active_google_places_list)

lat_lng_list = [(34.052235, -118.243683)]#, (40.748817, -73.985428),
                #(41.881832, -87.623177), (29.761993, -95.366302),
                #(39.952583, -75.165222)]


def iterate_lat_lng(lat_iterations=1, lng_iterations=1):
    results = dict()
    for start_lat, start_lng in lat_lng_list:
        for i in xrange(lat_iterations):
            for j in xrange(lng_iterations):
                print "Processing i: %s, j: %s" % (i, j)
                query_result = handle_api_request(start_lat + i * 0.01,
                                                  start_lng + j * 0.01)
                for place in query_result.places:
                    print "Preparing data for place: %s" % place.name
                    if place.place_id in results:
                        continue
                    try:
                        place.get_details()
                    except GooglePlacesError:
                        break
                    results[place.place_id] = {field: place.details.get(field, "")
                                               for field in set_of_fields_to_select}
                    photos_urls = list()
                    for photo in place.photos:
                        photo.get(maxheight=500, maxwidth=500)
                        photos_urls.append(photo.url)
                    results[place.place_id]["photos_urls"] = photos_urls
    persist_to_db(results)
    return results


def persist_to_db(results):
    for result in results.values():
        print "Persisting place: %s" % result["name"]
        soup = BeautifulSoup(result["adr_address"])
        country, is_created = Country.objects.get_or_create(name=soup.find("span", {"class": "region"}).next)
        city, is_created = City.objects.get_or_create(name=soup.find("span", {"class": "locality"}).next)
        location, is_created = Location.objects.get_or_create(type=LOCATION_TYPE.place.value,
                                           lat=round(result["geometry"]["location"]["lat"], 5),
                                           lng=round(result["geometry"]["location"]["lng"], 5),
                                           formatted_address=result["formatted_address"],
                                           country=country,
                                           city=city)
        types = list()
        for type in result["types"]:
            if type in relevant_types:
                types.append(Type.objects.get_or_create(name=type)[0])

        opening_hours_list = list()
        for daily_opening_hours in result["opening_hours"]["periods"]:
            open = daily_opening_hours["open"]
            close = daily_opening_hours["close"]
            opening_hours_list.append(
                OpeningHours.objects.get_or_create(day=open["day"],
                                                   open="%s:%s" % (open["time"][:2], open["time"][2:]),
                                                   close="%s:%s" % (close["time"][:2], close["time"][2:]))[0])

        place, is_created = Place.objects.get_or_create(name=result["name"], location=location,
                                     phone_number=result["international_phone_number"],
                                     rating=result["rating"], website=result["website"])
        place.types.add(*types)
        place.opening_hours.add(*opening_hours_list)
        for photo_url in result["photos_urls"]:
            Image.objects.get_or_create(url=photo_url, place=place)


def handle_api_request(lat, lng):
    now = datetime.utcnow()
    while True:
        if deactivated_keys and (now - deactivated_keys[-1][1]).total_seconds() > api_key_cool_down:
            deactivated_keys.pop()
        if len(deactivated_keys) == len(active_google_places_list):
            time.sleep(10)
            continue
        try:
            k, google_places = active_google_places_cycle.next()
            print "current api: %s" % google_places.api_key
            if any(k == i for i, last_updated in deactivated_keys):
                continue
            return google_places.nearby_search(lat_lng={"lat": lat, "lng": lng},
                                                        types=relevant_types,
                                                        radius=700)
        except GooglePlacesError:
            print "Deactivating api_key: %s" % google_places.api_key
            deactivated_keys.insert(0, (k, datetime.utcnow()))

if __name__ == '__main__':
    iterate_lat_lng()