OPENING_HOURS_AND_TYPE_QUERY = """
SELECT DISTINCT
    place.website,
    place.rating,
    place.name,
    location.formatted_address,
    place.id
FROM
    place
        INNER JOIN
    place_opening_hours ON (place.id = place_opening_hours.place_id)
        INNER JOIN
    openinghours ON (place_opening_hours.openinghours_id = openinghours.id)
        INNER JOIN
    place_types ON (place.id = place_types.place_id)
        INNER JOIN
    type ON (place_types.type_id = type.id)
        LEFT OUTER JOIN
    location ON (place.location_id = location.id)
WHERE
    (openinghours.day = %s
        AND (openinghours.open BETWEEN %s AND %s
        OR openinghours.close BETWEEN %s AND %s)
        AND type.name = %s)
ORDER BY place.rating DESC
"""

PLACE_DETAILS_QUERY = """
SELECT
*
FROM
   place
WHERE
   place.id = %s
"""

REVIEWS_DETAILS_QUERY = """
SELECT
*
FROM
    review
WHERE
    review.place_id = %s
"""

PLACE_FIRST_IMAGE_QUERY = """
SELECT
    image.url
FROM
    image
WHERE
    image.place_id = %s
LIMIT 1
"""

PLACE_TYPES_QUERY = """
SELECT
    type.*
FROM
    type
        INNER JOIN
    place_types ON (type.id = place_types.type_id)
WHERE
    place_types.place_id = %s
"""

PLACE_OPENING_HOURS_QUERY = """
SELECT
    *
FROM
    openinghours
        INNER JOIN
    place_opening_hours ON (openinghours.id = place_opening_hours.openinghours_id)
WHERE
    place_opening_hours.place_id = %s
ORDER BY
    openinghours.day
"""

AVG_STATS_QUERY = """
SELECT 
    type_name,
    city_name,
    count_rating,
    MAX(avg_rating) AS max_rating
FROM
    (SELECT
        city.name AS city_name,
            type.name AS type_name,
            AVG(review.rating) AS avg_rating,
            COUNT(review.rating) AS count_rating
    FROM
        place
    LEFT OUTER JOIN location ON (place.location_id = location.id)
    LEFT OUTER JOIN city ON (location.city_id = city.id)
    LEFT OUTER JOIN place_types ON (place.id = place_types.place_id)
    LEFT OUTER JOIN type ON (place_types.type_id = type.id)
    LEFT OUTER JOIN review ON (place.id = review.place_id)
    GROUP BY city.name , type.name
    HAVING AVG(review.rating) IS NOT NULL
        AND COUNT(review.rating) > 5
    ORDER BY type.name ASC , avg_rating DESC) avg_rating
GROUP BY type_name
ORDER BY max_rating DESC
"""


COUNT_STATS_QUERY = """
SELECT
    type_name,
    city_name,
    MAX(count_places) AS max_count
FROM
    (SELECT
        city.name AS city_name,
            type.name AS type_name,
            COUNT(place.name) AS count_places
    FROM
        place
    LEFT OUTER JOIN location ON (place.location_id = location.id)
    LEFT OUTER JOIN city ON (location.city_id = city.id)
    LEFT OUTER JOIN place_types ON (place.id = place_types.place_id)
    LEFT OUTER JOIN type ON (place_types.type_id = type.id)
    GROUP BY city.name , type.name
    ORDER BY type.name ASC , count_places DESC) count_places_table
GROUP BY type_name
ORDER BY max_count DESC
"""


PLACES_COUNT_QUERY = """
SELECT
    COUNT(*) as places_count
FROM
    place;
"""

REVIEWS_COUNT_QUERY = """
SELECT
    COUNT(*) as reviews_count
FROM
    review;
"""

IMAGES_COUNT_QUERY = """
SELECT
    COUNT(*) as images_count
FROM
    image;
"""

CITIES_COUNT_QUERY = """
SELECT
    COUNT(*) as cities_count
FROM
    city;
"""

REVIEWS_OVER_RATING_FOUR_QUERY = """
SELECT
    COUNT(*) as reviews_count
FROM
    review
WHERE review.rating >= 4.0
"""

PLACE_IMAGES_QUERY = """
SELECT 
    place.name, image.url
FROM
    place
        LEFT OUTER JOIN
    image ON (place.id = image.place_id)
WHERE
    place.id = %s
"""

NAME_SEARCH_QUERY = """
SELECT 
    location.formatted_address,
    place.website,
    place.name,
    place.id,
    place.rating
FROM
    place
        LEFT OUTER JOIN
    location ON (place.location_id = location.id)
WHERE
    MATCH (place.name) AGAINST (%s IN NATURAL LANGUAGE MODE)
"""

GEO_DISTANCE_AND_RATING_QUERY = """
SELECT
    place.id,
    place.name,
    location.formatted_address,
    place.rating,
    place.website,
    truncate((6371 * ACOS(COS(RADIANS(%s)) * COS(RADIANS(location.lat)) *
    COS(RADIANS(location.lng) - RADIANS(%s))
    + SIN(RADIANS(%s)) * SIN(RADIANS(location.lat)))), 3) AS distance
FROM
    place
        RIGHT OUTER JOIN
    location ON (place.location_id = location.id)
WHERE
    place.rating >= %s
HAVING distance <= %s
"""

FULL_SEARCH_QUERY = """
SELECT DISTINCT
    place.website,
    place.rating,
    place.name,
    location.formatted_address,
    place.id,
    truncate((6371 * ACOS(COS(RADIANS(%s)) * COS(RADIANS(location.lat)) *
    COS(RADIANS(location.lng) - RADIANS(%s))
    + SIN(RADIANS(%s)) * SIN(RADIANS(location.lat)))), 3) AS distance
FROM
    place
        INNER JOIN
    place_opening_hours ON (place.id = place_opening_hours.place_id)
        INNER JOIN
    openinghours ON (place_opening_hours.openinghours_id = openinghours.id)
        INNER JOIN
    place_types ON (place.id = place_types.place_id)
        INNER JOIN
    type ON (place_types.type_id = type.id)
        LEFT OUTER JOIN
    location ON (place.location_id = location.id)
WHERE
    (openinghours.day = %s
        AND (openinghours.open BETWEEN %s AND %s
        OR openinghours.close BETWEEN %s AND %s)
        AND type.name = %s
        AND place.rating >= %s)
HAVING distance <= %s
"""

INSERT_REVIEW_QUERY = """
INSERT INTO review (author_name, rating, text, place_id)
VALUES (%s, %s, %s, %s);
"""

INSERT_IMAGE_QUERY = """
INSERT INTO image (url, place_id)
VALUES (%s, %s);
"""