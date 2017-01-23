import os
import sys
from time import time

import MySQLdb as mdb
from django.http import HttpResponseRedirect
from django.shortcuts import render
from googleplaces import geocode_location, GooglePlacesError

from queries import OPENING_HOURS_AND_TYPE_QUERY, PLACE_DETAILS_QUERY, \
    REVIEWS_DETAILS_QUERY, PLACE_FIRST_IMAGE_QUERY, PLACE_TYPES_QUERY, PLACE_OPENING_HOURS_QUERY, AVG_STATS_QUERY, \
    PLACES_COUNT_QUERY, REVIEWS_COUNT_QUERY, CITIES_COUNT_QUERY, IMAGES_COUNT_QUERY, REVIEWS_OVER_RATING_FOUR_QUERY, \
    PLACE_IMAGES_QUERY, COUNT_STATS_QUERY, NAME_SEARCH_QUERY, GEO_DISTANCE_AND_RATING_QUERY, FULL_SEARCH_QUERY, \
    INSERT_REVIEW_QUERY, INSERT_IMAGE_QUERY

host = "mysqlsrv.cs.tau.ac.il"
user = "DbMysql13"
password = "DbMysql13"
dbname = "DbMysql13"
try:
    conn = mdb.connect(host, user, password, dbname)
    cur = conn.cursor()
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

NUMERIC_DAY_TO_NAME = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
FIELDS = ["website", "rating", "name", "location__formatted_address", "id"]


def redirect_to_homepage(request):
    return HttpResponseRedirect("/index")


def handle_times(start_time, end_time):
    start_time, start_ampm = start_time.split()
    end_time, end_ampm = end_time.split()
    start_time = "%s:%s" % (int(start_time.split(":")[0]) + 12, start_time.split(":")[1]) \
        if start_ampm == "PM" else start_time
    end_time = "%s:%s" % (int(end_time.split(":")[0]) + 12, end_time.split(":")[1]) \
        if end_ampm == "PM" else end_time
    start_time = "00:00" if start_time == "24:00" else start_time
    end_time = "00:00" if end_time == "24:00" else end_time
    return start_time, end_time


def get_results(cur):
    fields = [row[0] for row in cur.description]
    results = [dict({"numeric_id": numeric_id + 1}, **dict(zip(fields, place_tuple))) for numeric_id, place_tuple
               in enumerate(cur.fetchall())]
    return results


def get_images_slices(place_id):
    cur.execute(PLACE_IMAGES_QUERY, (place_id, ))
    results = get_results(cur)
    place_images = [result["url"] for result in results]
    place_name = results[0]["name"]
    quarter_count = len(place_images) // 4 + 1
    place_images = [place_images[quarter_count * i:quarter_count * (i + 1)] for i in xrange(4)]
    return place_name, place_images


def handle_uploaded_file(f, place_id):
    file_url = "/static/img/user_images/%s_%s" % (time(), f.name)
    with open("%s/%s" % (os.path.dirname(__file__), file_url), 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    cur.execute(INSERT_IMAGE_QUERY, (file_url, place_id))


def filter_places_by_opening_hours_and_type(request):
    results = list()
    searched_for_results = False
    is_distance_query = False
    if request.GET:
        day = int(request.GET.get("day"))
        start_time = request.GET.get("open_time")
        end_time = request.GET.get("close_time")
        place_type = request.GET.get("type")
        start_time, end_time = handle_times(start_time, end_time)
        cur.execute(OPENING_HOURS_AND_TYPE_QUERY, (day, start_time, end_time, start_time, end_time, place_type))
        results = get_results(cur)
        searched_for_results = True
    return render(request, 'typeOH.html', {"results": results,
                                           "searched_for_results": searched_for_results,
                                           "is_distance_query": is_distance_query})


def filter_places_by_address_and_rating(request):
    results = []
    searched_for_results = False
    is_distance_query = True
    if request.GET:
        rating = float(request.GET.get("rating"))
        address = request.GET.get("address")
        radius = int(request.GET.get("radius"))
        try:
            geo_location = geocode_location(address)
            lat = geo_location["lat"]
            lng = geo_location["lng"]
            order_by = request.GET.get("order_by")
            order_by_clause = "%s ASC" % order_by if order_by == "distance" else "rating DESC"
            query_with_order_by = "%s order by %s" % (GEO_DISTANCE_AND_RATING_QUERY, order_by_clause)
            cur.execute(query_with_order_by, (lat, lng, lat, rating, radius))
            results = get_results(cur)
            searched_for_results = True
        except GooglePlacesError, e:
            pass

    return render(request, 'ratingAddrRadius.html', {"results": results,
                                                     "searched_for_results": searched_for_results,
                                                     "is_distance_query": is_distance_query})


def filter_by_all_params(request):
    results = list()
    searched_for_results = False
    is_distance_query = True
    if request.GET:
        rating = request.GET.get("rating")
        address = request.GET.get("address")
        radius = int(request.GET.get("radius"))
        try:
            geo_location = geocode_location(address)
            lat = geo_location["lat"]
            lng = geo_location["lng"]
            day = int(request.GET.get("day"))
            start_time = request.GET.get("open_time")
            end_time = request.GET.get("close_time")
            place_type = request.GET.get("type")
            start_time, end_time = handle_times(start_time, end_time)
            order_by = request.GET.get("order_by")
            order_by_clause = "%s ASC" % order_by if order_by == "distance" else "rating DESC"
            query_with_order_by = "%s order by %s" % (FULL_SEARCH_QUERY, order_by_clause)
            cur.execute(query_with_order_by, (lat, lng, lat, day, start_time, end_time, start_time,
                                              end_time, place_type, rating, radius))
            results = get_results(cur)
            searched_for_results = True
        except GooglePlacesError, e:
            pass
    return render(request, 'detailsTable.html', {"results": results,
                                                 "searched_for_results": searched_for_results,
                                                 "is_distance_query": is_distance_query})


def insert_image(request):
    image = request.FILES.get("file")
    place_id = int(request.POST.get("place_id"))
    handle_uploaded_file(image, place_id)
    place_name, place_images = get_images_slices(place_id)
    return render(request, "gallery.html", {"place_name": place_name, "place_images": place_images,
                                            "place_id": place_id})


def insert_review(request):
    author_name = request.GET.get("author_name")
    place_id = int(request.GET.get("place_id"))
    rating = float(request.GET.get("rating"))
    text = request.GET.get("text")
    cur.execute(INSERT_REVIEW_QUERY, (author_name, rating, text, place_id))
    return HttpResponseRedirect('/place?place_id=%s' % place_id)


def home_page_stats(request):
    cur.execute(PLACES_COUNT_QUERY)
    places_count = get_results(cur)[0]["places_count"]
    cur.execute(REVIEWS_COUNT_QUERY)
    reviews_count = get_results(cur)[0]["reviews_count"]
    cur.execute(IMAGES_COUNT_QUERY)
    images_count = get_results(cur)[0]["images_count"]
    cur.execute(CITIES_COUNT_QUERY)
    cities_count = get_results(cur)[0]["cities_count"]
    cur.execute(REVIEWS_OVER_RATING_FOUR_QUERY)
    reviews_over_rating_four = get_results(cur)[0]["reviews_count"]
    return render(request, 'index.html', {"places_count": places_count, "reviews_count": reviews_count,
                                          "images_count": images_count, "cities_count": cities_count,
                                          "reviews_perc_over_four":
                                              int(float(reviews_over_rating_four) / reviews_count * 100)})


def get_complicated_stats(request):
    cur.execute(AVG_STATS_QUERY)
    avg_rating_results = get_results(cur)
    cur.execute(COUNT_STATS_QUERY)
    count_rating_results = get_results(cur)
    return render(request, 'statistics.html', {"avg_results": avg_rating_results,
                                               "count_results": count_rating_results})


def get_place_details(request):
    place_id = int(request.GET.get("place_id"))
    cur.execute(PLACE_DETAILS_QUERY, (place_id, ))
    place_details = get_results(cur)[0]
    place_details["place_id"] = place_details["id"]
    cur.execute(REVIEWS_DETAILS_QUERY, (place_id, ))
    place_details["reviews"] = get_results(cur)
    cur.execute(PLACE_FIRST_IMAGE_QUERY, (place_id, ))
    images_result = get_results(cur)
    place_details["image_url"] = images_result[0]["url"] if images_result \
        else "https://www.raise.sg/membership/web/images/noimage.jpg"
    cur.execute(PLACE_TYPES_QUERY, (place_id, ))
    place_details["types"] = get_results(cur)
    cur.execute(PLACE_OPENING_HOURS_QUERY, (place_id, ))
    place_details["opening_hours_list"] = [dict(result, **{"day": NUMERIC_DAY_TO_NAME[result["day"]]})
                                           for result in get_results(cur)]
    return render(request, "place.html", place_details)


def get_place_images(request):
    place_id = int(request.GET.get("place_id"))
    place_name, place_images = get_images_slices(place_id)
    return render(request, "gallery.html", {"place_name": place_name, "place_images": place_images,
                                            "place_id": place_id})


def text_search(request):
    results = []
    searched_for_results = False
    if request.GET:
        text = request.GET.get("text")
        cur.execute(NAME_SEARCH_QUERY, (text, ))
        results = get_results(cur)
        searched_for_results = True
    return render(request, "textSearch.html", {"results": results,
                                               "searched_for_results": searched_for_results})

