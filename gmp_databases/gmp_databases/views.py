from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from models import Place, Review, Image, City
from django.db.models import Q, Avg, Count


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


def get_results(places):
    results = [dict({"numeric_id": numeric_id + 1}, **place_dict) for numeric_id, place_dict
               in enumerate(places.values(*FIELDS))]
    return results


def filter_places_by_opening_hours_and_type(request):
    day = request.GET.get("day")
    start_time = request.GET.get("open_time")
    end_time = request.GET.get("close_time")
    place_type = request.GET.get("type")
    order_by = None
    limit = None
    if day:
        start_time, end_time = handle_times(start_time, end_time)
        places = get_filter_by_opening_hours(Place.objects, day, start_time, end_time)
        places = places.filter(types__name=place_type)
        places = get_ordered_limited_places(places, order_by, limit)
        results = get_results(places)
        searched_for_results = True
    else:
        results = list()
        searched_for_results = False
    return render(request, 'typeOH.html', {"results": results,
                                           "searched_for_results": searched_for_results})


def filter_places_by_address_and_rating(request, address, radius, bottom_rating, order_by, limit):
    places = Place.objects.filter(rating__gt=bottom_rating)
    places = get_ordered_limited_places(places, order_by, limit)
    return render(request, 'first_html.html', {'results': list(places.values())})


def filter_by_all_params(request, day, starttime, endtime,
                         address, radius, bottom_rating, type_name, order_by, limit):
    places = Place.objects.filter(rating__gt=bottom_rating)
    places = get_filter_by_opening_hours(places, day, starttime, endtime)
    places = places.filter(types__name=type_name)
    places = get_ordered_limited_places(places, order_by, limit)
    return render(request, 'first_html.html', {'results': list(places.values())})


def insert_image(request):
    f = request.POST.get("image")


def insert_review(request):
    author_name = request.POST.get("author_name")
    place_id = request.POST.get("place_id")
    rating = request.POST.get("rating")
    text = request.POST.get("text")
    Review.objects.create(author_name=author_name, place_id=place_id, rating=rating, text=text)
    return HttpResponseRedirect(reverse("first_html.html"))


def home_page_stats(request):
    places_count = Place.objects.count()
    reviews_count = Review.objects.count()
    images_count = Image.objects.count()
    cities_count = City.objects.count()
    reviews_over_rating_four = Review.objects.filter(rating__gt=4).count()
    return render(request, 'index.html', {"places_count": places_count, "reviews_count": reviews_count,
                                          "images_count": images_count, "cities_count": cities_count,
                                          "reviews_perc_over_four":
                                              int(float(reviews_over_rating_four) / reviews_count * 100)})


def get_complicated_stats(request):
    filtered_places = Place.objects.all().values("location__city__name",
                                                 "types__name")\
                           .annotate(avg_rating=Avg('rating'), count_rows=Count("rating")) \
                           .filter(avg_rating__gt=4)
    return render(request, 'html', list(filtered_places))


def get_place_details(request):
    place_id = request.GET.get("place_id")
    place = Place.objects.filter(id=place_id)
    place_details = place.values().first()
    place = place.first()
    place_details["reviews"] = place.review_set.values()
    place_details["image_url"] = place.image_set.values_list("url", flat=True).first() \
        or "https://www.raise.sg/membership/web/images/noimage.jpg"
    place_details["types"] = place.types.values()
    place_details["opening_hours_list"] = place.opening_hours.values()
    return render(request, "place.html", place_details)


def get_place_images(request):
    place_id = request.GET.get("place_id")
    place = Place.objects.get(id=place_id)
    place_images = Place.objects.values_dict("images__url", flat=True).get(id=place_id)
    return render(request, "gallery.html", {"place_name": place.name, "place_images": place_images})
