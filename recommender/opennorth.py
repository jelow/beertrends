import logging
import requests

logger = logging.getLogger('api_interface.brewerydb')

BASE_URL = "https://represent.opennorth.ca/postcodes/"

def query_postcode(postcode):
    """Makes an API request to OpenNorth with the specified postal code.

    Args:
        postcode -  the postcode to query. It must be of the form
                    A1A1A1 -- all upper-case with no spaces.

    Returns:
        A dictionary of the form { "lat": 49.0, "lng": 123.0 }
    """

    url = BASE_URL + postcode

    logger.debug('Making request to ' + url)

    r = requests.get(url, {"format": "json"})

    json = r.json()

    lng = json['centroid']['coordinates'][0]
    lat = json['centroid']['coordinates'][1]

    logger.debug('Got coordinates. Lat: ' + str(lat) + '. Lng: ' + str(lng))

    return { "lat": lat, "lng": lng }

