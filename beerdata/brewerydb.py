import logging
import requests

logger = logging.getLogger('beerdata.brewerydb')

BASE_URL = "http://api.brewerydb.com/v2/"
API_KEY = "d40a758bc2d06332847e932cc1311e47"

def search(search_type, brewery_id, search_str):
    logger.info('Searching for {} with string {}'.format(search_type, search_str))

    params = {'q': search_str, 'type': search_type}

    if brewery_id:
        params['withBreweries'] = 'Y'

    page = 1
    numPages = 50
    maxPages = 1
    return_list = []

    while page <= numPages and page <= maxPages:
        params['p'] = page
        q = query('/search', params)
        if 'numberOfPages' in q:
            numPages = q['numberOfPages']
        logger.debug('Fetching page {} of {}.'.format(page, numPages))
        page += 1

        if 'data' in q:
            for item in q['data']:
                if brewery_id and 'breweries' in item:
                    for brewery in item['breweries']:
                        if brewery['id'] == brewery_id:
                            return_list.append({'id': item['id'], 'name': item['name']})
                else:
                    return_list.append({'id': item['id'], 'name': item['name']})

    if return_list == []:
        return None
    return return_list

def query_brewery(breweryId):
    """Gets a brewery

    Args:
    breweryId - the ID of the brewery to retrieve

    Returns:
    A dictionary
    """
    logger.info('Querying for brewery with ID ' + breweryId)
    q = query('/brewery/' + str(breweryId), {'withLocations': 'Y'})

    if 'data' in q:
        data = q['data']
        return {'id': data['id'], 'name': data['name'], 'latitude': data['locations'][0]['latitude'],
                'longitude': data['locations'][0]['latitude']}
    else:
        logger.warn('Brewery not found.')
        return {}


def query_beer(beerId):
    """Gets a beer

    Args:
    beerId - the ID of the beer to retrieve

    Returns:
    A dictionary
    """
    logger.info('Querying for beer with ID ' + beerId)
    q = query('/beer/' + str(beerId), {})

    if 'data' in q:
        return q['data']
    else:
        logger.warn('Beer not found.')
        return {}

def query_style(styleId):
    """Gets a style

    Args:
    styleId - the ID of the style to retrieve

    Returns:
    A dictionary
    """
    q = query('/style/' + str(styleId), {})

    if 'data' in q:
        return q['data']
    else:
        return {}


def query_brewery_beers(breweryId):
    """Gets all the beers a brewery makes.

    Args:
    breweryId  - the ID of the brewery to query

    Returns:
    A list of dictionaries
    """

    q = query('/brewery/' + breweryId + '/beers', {})
    
    if 'data' in q:
        return q['data']
    else:
        return []


def query_nearby_breweries(lat, lng, radius):
    """Gets all breweries within a certain radius of a point

    Args:
    lat     - the latitude of the point
    lng     - the longitude of the point
    radius  - the radius in kilometers

    Returns:
    A list of dictionaries
    """
    logger.debug('Querying for breweries within ' + str(radius) + ' kilometers of ' + str(lat) + ', ' + str(lng))

    # Get the raw data
    q = query('/search/geo/point', {'lat': lat, 'lng': lng, 'radius':
        radius, 'unit': 'km'})

    # Put all breweries into one list (remove pagination)
    if 'data' in q:
        return q['data']
    else:
        return []


def query(endpoint, get_params):
    """Makes an API request URL with the specified endpoint and GET
    parameters.

    Args:
    endpoint   - String. Must be one of the BreweryDb API endpoints
    get_params - Dictionary. Keys must be a valid request parameter for the speficied endpoint.

    Returns:
    A dictionary
    """

    url = BASE_URL + endpoint
    get_params['key'] = API_KEY

    r = requests.get(url, params=get_params)

    return r.json()

