import mysql.connector
import os
from time import time

from django.db.models import Q
from django.shortcuts import render

from queries import OPENING_HOURS_AND_TYPE_QUERY, PLACE_DETAILS_QUERY, \
    REVIEWS_DETAILS_QUERY, PLACE_FIRST_IMAGE_QUERY, PLACE_TYPES_QUERY, PLACE_OPENING_HOURS_QUERY, AVG_STATS_QUERY, \
    PLACES_COUNT_QUERY, REVIEWS_COUNT_QUERY, CITIES_COUNT_QUERY, IMAGES_COUNT_QUERY, REVIEWS_OVER_RATING_FOUR_QUERY, \
    PLACE_IMAGES_QUERY
from models import Place, Review, Image

host = "mysqlsrv.cs.tau.ac.il"
user = "DbMysql13"
password = "DbMysql13"
dbname = "DbMysql13"
try:
    conn = mysql.connector.connect(host=host, database=dbname, user=user, password=password)
    if conn.is_connected():
        print('Connected to MySQL database')
    cur = conn.cursor()
except mysql.connector.Error:
    pass

NUMERIC_DAY_TO_NAME = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
FIELDS = ["website", "rating", "name", "location__formatted_address", "id"]


def get_filter_by_opening_hours(places, day, starttime, endtime):
    return places.filter(Q(opening_hours__day=day) & Q(
        Q(opening_hours__open__range=(starttime, endtime)) | Q(opening_hours__close__range=(starttime, endtime)))) \
        .distinct()


def get_ordered_limited_places(places, order_by, limit):
    limit = limit or 100
    order_by = order_by or "rating"
    places = places.order_by("-%s" % order_by)
    return places[:limit]


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
    Image.objects.create(url=file_url, place_id=place_id)


def filter_places_by_opening_hours_and_type(request):
    day = int(request.GET.get("day"))
    start_time = request.GET.get("open_time")
    end_time = request.GET.get("close_time")
    place_type = request.GET.get("type")
    # order_by = None
    # limit = None
    if day:
        start_time, end_time = handle_times(start_time, end_time)
        cur.execute(OPENING_HOURS_AND_TYPE_QUERY, (day, start_time, end_time, start_time, end_time, place_type))
        results = get_results(cur)
        searched_for_results = True
    else:
        results = list()
        searched_for_results = False
    return render(request, 'typeOH.html', {"results": results,
                                           "searched_for_results": searched_for_results})


def filter_places_by_address_and_rating(request, address, radius, bottom_rating, order_by, limit):
    places = Place.objects.filter(rating__gt=bottom_rating)
    places = get_ordered_limited_places(places, order_by, limit)
    return render(request, 'ratingAddrRadius.html', {'results': list(places.values())})


def filter_by_all_params(request, day, starttime, endtime,
                         address, radius, bottom_rating, type_name, order_by, limit):
    places = Place.objects.filter(rating__gt=bottom_rating)
    places = get_filter_by_opening_hours(places, day, starttime, endtime)
    places = places.filter(types__name=type_name)
    places = get_ordered_limited_places(places, order_by, limit)
    return render(request, 'detailsTable.html', {'results': list(places.values())})


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
    Review.objects.create(author_name=author_name, place_id=place_id, rating=rating, text=text)
    return get_place_details(request)


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
    return render(request, 'html', get_results(cur))


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
