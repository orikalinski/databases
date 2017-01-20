import os
import time
from datetime import datetime
from itertools import cycle

from bs4 import BeautifulSoup
from googleplaces import GooglePlaces, types, GooglePlacesError

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "gmp_databases.gmp_databases.settings")

from gmp_databases.gmp_databases.models import Place, \
    Image, Country, City, Type, Location, LOCATION_TYPE, OpeningHours, Review

api_keys = ["AIzaSyAu4PKwcADVNSbjkfs6wOcxNeEHtHO6boQ",
            "AIzaSyD9asahayiUzfBCYv4GjKyoROpjwUraDgU",
            "AIzaSyBeioFH_Q9bHmeGP6NAe9-_uQ_jNzdTLI4",
            "AIzaSyB671Kz34WvM5sup8WiDp5hkL87NkH1YFk",
            "AIzaSyBkugashcLD99dtakYiaDO9VumebhKV5rs",
            "AIzaSyAxLCkEDmsb115N11htTUhC62aHtmG_6Qw",
            "AIzaSyADuSCmHpFUUsa2yZvbSLLs6eOEQVWonrQ",
            "AIzaSyAjNeXvlytwEqngj_OucF3GxaY6vJUhNpw",
            "AIzaSyC5b1etMPL7i8z8RJ8YP_eexpOQxSO1rpw",
            'AIzaSyAkRwvJb9_dKg_rIA3txbeKeFggnAOvf6s',
            'AIzaSyAY0uG0iVANACHwnGYENlCWjcjqveAf-y0',
            'AIzaSyA05M3g7yBczb67hVeKj5LF8AhyzjmS6UA',
            'AIzaSyALNAuJFyHWYjfr1odDDVcA-LKc7yW6aUE',
            'AIzaSyDqNziyDXO7xtUFqWiZ_BT2z8OiWJXhQdU',
            'AIzaSyBPvrgWZme9vrFVu2qiNvZMLxi4VB208mc',
            'AIzaSyDXo4NIywNC5XWfwS8qsxZ7D9ptes_ikD8',
            'AIzaSyBRwEC-DvM--glkqRuHFdH3tkPp5k1al9Q',
            'AIzaSyCkFeBF8Jw7S-lm7TyAQlSmwGAxUFDpeRk',
            'AIzaSyAz-fR2AujhanX4Z-3Z9nbJzTdiq76OLJ0',
            'AIzaSyBf6K0t5uIvc69Cq_Y8QvIgVIzTHHZaPIs',
            'AIzaSyDkZ27YGVuZzO8KiuWBfARcjg-QcUqbt7s',
            'AIzaSyAk4OOQal22pnqWI1kpMr6ZQkjR-eYUmdE',
            'AIzaSyDv4LrANg4q3Cz35BYfWC1JA7CLqMVjopA',
            'AIzaSyAMJLrdIFdjAe-b-Sb8gq1ilfFu0Kouj14',
            'AIzaSyB5Qc0QXhJTyYUuTS1gM9mBpDZ7q7nq6FI',
            'AIzaSyAVkzrXDvDgZdUitMtAbMeoRAt8RAMFchA',
            'AIzaSyD5Rpt-wxg9jxddF_kb38hOfVK-XFaOC-o',
            'AIzaSyAqiuC2QHsEWqch6p8sTWLUvwJWUQqnYHU',
            'AIzaSyAUBUBC24_TCSuqo35TzsRfTJdhQL1Usm0',
            'AIzaSyBYXZe_xHvP5Xr1HFJ27nsP1MOYhXVaYss',
            'AIzaSyAx8G5mB2Cjg5WPHIU4hfj2qcBpcOhnkPo',
            'AIzaSyAQdKwimbJOSxijyS4ldF8OMZEDEGML06Y',
            'AIzaSyAqwVIL2KwMuCmvZkg3ExC5tMa5IP3_pWI',
            'AIzaSyArNEbSfCjbE5bYEPqDfA7dkc5hL8aMPwM',
            'AIzaSyBcu58nZMrW1nSuG-LOC1RzXDWWei7xgiU',
            'AIzaSyDWkRDSsHbS2MPt72lygvT1ix1IapXowAw',
            'AIzaSyD8EbBWAAXSQHUF_1Eu1YHdZ84Wg5pOwho',
            'AIzaSyAkCJkBhyL-zksnO0FLeCo7b3BN1V9879U',
            'AIzaSyCRjq7w5A2i-oN5rOsO3M7VBBPzi13LXKg',
            'AIzaSyDrX6GqlgBHiP1xznMeIlpjEjyjY8kRB_4',
            'AIzaSyB3Amn952TXw8c8UBh6RbSGVhm5Zm5g42Q',
            'AIzaSyDM5xdghYsNQ7_OkL5wvoeX57_odizN78s',
            'AIzaSyA882YHIWfDaaSiR_sNjU3uNFUuMZmKbBo',
            'AIzaSyDBcejbCyTOTVwYrbBgAIvc7BqLKuYOsRs',
            'AIzaSyC8TG7K0JZF-wfm3Gxz82qRnK1elbsqlbI',
            'AIzaSyDo98ezPzzKKpTd2wpMs-RBju-Mlnt2k2o',
            'AIzaSyBTg5hzxZRMoJuOLuqGZOOAcRKPto73R2g',
            'AIzaSyCtz-Q4wOYyl3fXeQdSnxd6CoCt0Q2etaE',
            'AIzaSyCUBRhs5ZOGBc2lJOblX67CQgjoKZJU5dQ',
            'AIzaSyALWCKTKugPWvQYKDNi7MTgIoa8MQg9T1w',
            'AIzaSyB5QT7qPx6vwJLJPqaQwjPPwf-YwgxJnEo',
            'AIzaSyANef9RhymhCZm6itzDuyNua6toHl92zbc',
            'AIzaSyCpBsB3mEKkt5l3Nxv2Ei3LQ6FBLnmoB44',
            'AIzaSyDMztQ1Ut-OFN5yRbwOYmD01k4XFR_7jqI',
            'AIzaSyBsC65oI9O7sLCz2l9XgDz_B_reowNcz5g',
            'AIzaSyBcQ1lKujePI4GM1M2bMuUhYbm424GzncM']

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

lat_lng_list = [(40.748817, -73.985428),
                (41.881832, -87.623177), (29.761993, -95.366302),
                (39.952583, -75.165222), (34.052235, -118.243683)]


def iterate_lat_lng(initial_lat_index, lat_iterations,
                    initial_lng_index, lng_iterations,
                    initial_lat_lng_index, enable_photos=True):
    processed_place_ids = set()
    for i in xrange(initial_lat_index, lat_iterations):
        for j in xrange(initial_lng_index, lng_iterations):
            for start_lat, start_lng in lat_lng_list[initial_lat_lng_index:]:
                results = dict()
                print "Processing start_lat: %s, start_lng:%s, i: %s, j: %s" % (start_lat, start_lng, i, j)
                query_result = handle_api_request(start_lat + i * 0.01,
                                                  start_lng + j * 0.01)
                for place in query_result.places:
                    if place.place_id in processed_place_ids:
                        continue
                    print "Preparing data for place: %s" % place.name
                    processed_place_ids.add(place.place_id)
                    try:
                        place.get_details()
                    except GooglePlacesError:
                        break
                    results[place.place_id] = {field: place.details.get(field)
                                               for field in set_of_fields_to_select}
                    photos_urls = list()
                    if enable_photos:
                        for photo in place.photos:
                            try:
                                photo.get(maxheight=500, maxwidth=500)
                                photos_urls.append(photo.url)
                            except Exception, e:
                                print "Warning: %s" % e
                                continue
                    results[place.place_id]["photos_urls"] = photos_urls
                persist_to_db(results)
        initial_lng_index = 0


def persist_to_db(results):
    for result in results.values():
        try:
            print "Persisting place: %s" % result["name"]
            adr_address = result.get("adr_address")
            country = city = None
            if adr_address:
                soup = BeautifulSoup(adr_address)
                country, is_created = Country.objects.get_or_create(name=soup.find("span", {"class": "region"}).next)
                city, is_created = City.objects.get_or_create(name=soup.find("span", {"class": "locality"}).next)
            location, is_created = Location.objects.get_or_create(type=LOCATION_TYPE.place.value,
                                               lat=round(result["geometry"]["location"]["lat"], 5),
                                               lng=round(result["geometry"]["location"]["lng"], 5),
                                               formatted_address=result.get("formatted_address"),
                                               country=country,
                                               city=city)
            types = list()
            for type in result["types"]:
                if type in relevant_types:
                    types.append(Type.objects.get_or_create(name=type)[0])

            opening_hours_list = list()
            opening_hours = result["opening_hours"]
            if opening_hours and opening_hours.get("periods"):
                for daily_opening_hours in opening_hours["periods"]:
                    open = daily_opening_hours["open"]
                    close = daily_opening_hours.get("close")
                    opening_hours_list.append(
                        OpeningHours.objects.get_or_create(day=open["day"],
                                                           open="%s:%s" % (open["time"][:2], open["time"][2:]),
                                                           close="%s:%s" % (close["time"][:2],
                                                                            close["time"][2:]) if close else None)[0])

            place, is_created = Place.objects.get_or_create(name=result["name"], location=location,
                                                            phone_number=result.get("international_phone_number"),

                                                            rating=result.get("rating"), website=result.get("website"))
            place.types.add(*types)
            place.opening_hours.add(*opening_hours_list)

            reviews = result.get("reviews")
            if reviews:
                for review in reviews:
                    Review.objects.get_or_create(author_name=review["author_name"],
                                                 rating=review["rating"],
                                                 text=review["text"],
                                                 place=place)

            for photo_url in result["photos_urls"]:
                Image.objects.get_or_create(url=photo_url, place=place)
        except Exception, e:
            print "Failed to insert: %s to db, %s" % (result["name"], e)


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
            if any(k == i for i, last_updated in deactivated_keys):
                continue
            print "current api: %s" % google_places.api_key
            return google_places.nearby_search(lat_lng={"lat": lat, "lng": lng},
                                                        types=relevant_types,
                                                        radius=700)
        except GooglePlacesError:
            print "Deactivating api_key: %s" % google_places.api_key
            deactivated_keys.insert(0, (k, datetime.utcnow()))

if __name__ == '__main__':
    iterate_lat_lng(initial_lat_index=51, lat_iterations=70,
                    initial_lng_index=50, lng_iterations=70,
                    initial_lat_lng_index=0, enable_photos=True)