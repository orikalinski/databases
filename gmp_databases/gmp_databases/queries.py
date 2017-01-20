OPENING_HOURS_AND_TYPE_QUERY = """
SELECT DISTINCT
    gmp_databases_place.website,
    gmp_databases_place.rating,
    gmp_databases_place.name,
    gmp_databases_location.formatted_address,
    gmp_databases_place.id
FROM
    gmp_databases_place
        INNER JOIN
    gmp_databases_place_opening_hours ON (gmp_databases_place.id = gmp_databases_place_opening_hours.place_id)
        INNER JOIN
    gmp_databases_openinghours ON (gmp_databases_place_opening_hours.openinghours_id = gmp_databases_openinghours.id)
        INNER JOIN
    gmp_databases_place_types ON (gmp_databases_place.id = gmp_databases_place_types.place_id)
        INNER JOIN
    gmp_databases_type ON (gmp_databases_place_types.type_id = gmp_databases_type.id)
        LEFT OUTER JOIN
    gmp_databases_location ON (gmp_databases_place.location_id = gmp_databases_location.id)
WHERE
    (gmp_databases_openinghours.day = %s
        AND (gmp_databases_openinghours.open BETWEEN %s AND %s
        OR gmp_databases_openinghours.close BETWEEN %s AND %s)
        AND gmp_databases_type.name = %s)
ORDER BY gmp_databases_place.rating DESC
"""

PLACE_DETAILS_QUERY = """
SELECT
*
FROM
   gmp_databases_place
WHERE
   gmp_databases_place.id = %s
"""

REVIEWS_DETAILS_QUERY = """
SELECT
*
FROM
    gmp_databases_review
WHERE
    gmp_databases_review.place_id = %s
"""

PLACE_FIRST_IMAGE_QUERY = """
SELECT
    gmp_databases_image.url
FROM
    gmp_databases_image
WHERE
    gmp_databases_image.place_id = %s
LIMIT 1
"""

PLACE_TYPES_QUERY = """
SELECT
    gmp_databases_type.*
FROM
    gmp_databases_type
        INNER JOIN
    gmp_databases_place_types ON (gmp_databases_type.id = gmp_databases_place_types.type_id)
WHERE
    gmp_databases_place_types.place_id = %s
"""

PLACE_OPENING_HOURS_QUERY = """
SELECT
    *
FROM
    gmp_databases_openinghours
        INNER JOIN
    gmp_databases_place_opening_hours ON (gmp_databases_openinghours.id = gmp_databases_place_opening_hours.openinghours_id)
WHERE
    gmp_databases_place_opening_hours.place_id = %s
ORDER BY
    gmp_databases_openinghours.day
"""

AVG_STATS_QUERY = """
SELECT 
    type_name,
    city_name,
    count_rating,
    MAX(avg_rating) AS max_rating
FROM
    (SELECT
        gmp_databases_city.name AS city_name,
            gmp_databases_type.name AS type_name,
            AVG(gmp_databases_review.rating) AS avg_rating,
            COUNT(gmp_databases_review.rating) AS count_rating
    FROM
        gmp_databases_place
    LEFT OUTER JOIN gmp_databases_location ON (gmp_databases_place.location_id = gmp_databases_location.id)
    LEFT OUTER JOIN gmp_databases_city ON (gmp_databases_location.city_id = gmp_databases_city.id)
    LEFT OUTER JOIN gmp_databases_place_types ON (gmp_databases_place.id = gmp_databases_place_types.place_id)
    LEFT OUTER JOIN gmp_databases_type ON (gmp_databases_place_types.type_id = gmp_databases_type.id)
    LEFT OUTER JOIN gmp_databases_review ON (gmp_databases_place.id = gmp_databases_review.place_id)
    GROUP BY gmp_databases_city.name , gmp_databases_type.name
    HAVING AVG(gmp_databases_review.rating) IS NOT NULL
        AND COUNT(gmp_databases_review.rating) > 5
    ORDER BY gmp_databases_type.name ASC , avg_rating DESC) avg_rating
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
        gmp_databases_city.name AS city_name,
            gmp_databases_type.name AS type_name,
            COUNT(gmp_databases_place.name) AS count_places
    FROM
        gmp_databases_place
    LEFT OUTER JOIN gmp_databases_location ON (gmp_databases_place.location_id = gmp_databases_location.id)
    LEFT OUTER JOIN gmp_databases_city ON (gmp_databases_location.city_id = gmp_databases_city.id)
    LEFT OUTER JOIN gmp_databases_place_types ON (gmp_databases_place.id = gmp_databases_place_types.place_id)
    LEFT OUTER JOIN gmp_databases_type ON (gmp_databases_place_types.type_id = gmp_databases_type.id)
    GROUP BY gmp_databases_city.name , gmp_databases_type.name
    ORDER BY gmp_databases_type.name ASC , count_places DESC) count_places_table
GROUP BY type_name
ORDER BY max_count DESC
"""


PLACES_COUNT_QUERY = """
SELECT
    COUNT(*) as places_count
FROM
    gmp_databases_place;
"""

REVIEWS_COUNT_QUERY = """
SELECT
    COUNT(*) as reviews_count
FROM
    gmp_databases_review;
"""

IMAGES_COUNT_QUERY = """
SELECT
    COUNT(*) as images_count
FROM
    gmp_databases_image;
"""

CITIES_COUNT_QUERY = """
SELECT
    COUNT(*) as cities_count
FROM
    gmp_databases_city;
"""

REVIEWS_OVER_RATING_FOUR_QUERY = """
SELECT
    COUNT(*) as reviews_count
FROM
    gmp_databases_review
WHERE gmp_databases_review.rating >= 4.0
"""

PLACE_IMAGES_QUERY = """
SELECT 
    gmp_databases_place.name, gmp_databases_image.url
FROM
    gmp_databases_place
        LEFT OUTER JOIN
    gmp_databases_image ON (gmp_databases_place.id = gmp_databases_image.place_id)
WHERE
    gmp_databases_place.id = %s
"""

NAME_SEARCH_QUERY = """
SELECT 
    gmp_databases_location.formatted_address,
    gmp_databases_place.website,
    gmp_databases_place.name,
    gmp_databases_place.id,
    gmp_databases_place.rating
FROM
    gmp_databases_place
        LEFT OUTER JOIN
    gmp_databases_location ON (gmp_databases_place.location_id = gmp_databases_location.id)
WHERE
    MATCH (gmp_databases_place.name) AGAINST (%s IN NATURAL LANGUAGE MODE)
"""

GEO_DISTANCE_AND_RATING_QUERY = """
SELECT
    gmp_databases_place.id,
    gmp_databases_place.name,
    gmp_databases_location.formatted_address,
    gmp_databases_place.rating,
    gmp_databases_place.website,
    truncate((6371 * ACOS(COS(RADIANS(%s)) * COS(RADIANS(gmp_databases_location.lat)) *
    COS(RADIANS(gmp_databases_location.lng) - RADIANS(%s))
    + SIN(RADIANS(%s)) * SIN(RADIANS(gmp_databases_location.lat)))), 3) AS distance
FROM
    gmp_databases_place
        RIGHT OUTER JOIN
    gmp_databases_location ON (gmp_databases_place.location_id = gmp_databases_location.id)
WHERE
    gmp_databases_place.rating >= %s
HAVING distance <= %s
"""

FULL_SEARCH_QUERY = """
SELECT DISTINCT
    gmp_databases_place.website,
    gmp_databases_place.rating,
    gmp_databases_place.name,
    gmp_databases_location.formatted_address,
    gmp_databases_place.id,
    truncate((6371 * ACOS(COS(RADIANS(%s)) * COS(RADIANS(gmp_databases_location.lat)) *
    COS(RADIANS(gmp_databases_location.lng) - RADIANS(%s))
    + SIN(RADIANS(%s)) * SIN(RADIANS(gmp_databases_location.lat)))), 3) AS distance
FROM
    gmp_databases_place
        INNER JOIN
    gmp_databases_place_opening_hours ON (gmp_databases_place.id = gmp_databases_place_opening_hours.place_id)
        INNER JOIN
    gmp_databases_openinghours ON (gmp_databases_place_opening_hours.openinghours_id = gmp_databases_openinghours.id)
        INNER JOIN
    gmp_databases_place_types ON (gmp_databases_place.id = gmp_databases_place_types.place_id)
        INNER JOIN
    gmp_databases_type ON (gmp_databases_place_types.type_id = gmp_databases_type.id)
        LEFT OUTER JOIN
    gmp_databases_location ON (gmp_databases_place.location_id = gmp_databases_location.id)
WHERE
    (gmp_databases_openinghours.day = %s
        AND (gmp_databases_openinghours.open BETWEEN %s AND %s
        OR gmp_databases_openinghours.close BETWEEN %s AND %s)
        AND gmp_databases_type.name = %s
        AND gmp_databases_place.rating >= %s)
HAVING distance <= %s
"""