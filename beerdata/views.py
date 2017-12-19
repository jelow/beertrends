import logging
import hashlib
import json
from django.http import HttpResponse
from . import brewerydb, update_beer, update_brewery
from .models import Beer
from trends.models import Rating

logger = logging.getLogger('beerdata.views')

HTTP_STATUS_DENIED = 403
MAX_RESULTS = 5

def search_beers(request):
    logger.info('Starting beer search.')

    if request.method == 'GET':
        query = request.GET.get('q')
        if not query:
            logger.error('Empty query. Returning empty dict.')
            return HttpResponse(json.dumps({}), content_type="application/json")
        result = fetch_beers(query)
        return HttpResponse(json.dumps(result), content_type="application/json")
        
    else:
        logger.error('Malformed request. Returning empty dict.')
        return HttpResponse(json.dumps({}), content_type="application/json")

def handle_update_beer(request):
    logger.info('Update beer web hook received.')

    # Ensure the request is coming from BreweryDb
    if not validate_request(request):
        logger.warn('Invalid request. Aborting.')
        return HttpResponse(status = HTTP_STATUS_DENIED);

    action = request.POST.get('action')
    beerId = request.POST.get('attributeId')

    if not beerId or not action:
        logger.error('Invalid request. Aborting.')

    # Handle beer updates
    elif action is 'edit':
        logger.info('Updating beer ' + beerId)
        update_beer.update_beer(beerId, update=True)

    logger.info('Completed web hook.')
    return HttpResponse()

    
def handle_update_brewery(request):
    logger.info('Update beer web hook received.')

    # Ensure the request is coming from BreweryDb
    if not validate_request(nonce, key):
        logger.warn('Invalid request. Aborting.')
        return HttpResponse(status = HTTP_STATUS_DENIED);

    breweryId = request.POST.get('attributeId')
    action = request.POST.get('action')
    subAction = request.POST.get('subAction')

    if not beerId or not action:
        logger.error('Invalid request. Aborting.')

    # Only handle edits to breweries
    if action is 'edit':
        logger.info('Updating brewery ' + breweryId)
        update_brewery.update_brewery(breweryId, update=True)

    # Handle new beer added to brewery
    elif action is 'insert' and subAction is 'beer-insert':
        beerId = request.POST.get('subAttributeId')
        if not beerId:
            logger.error('No beer ID provided')
        else:
            logger.info('New beer {} added to brewery {}'.format(beerId, breweryId))
            update_brewery.new_beer(beerId, breweryId)

    logger.info('Completed web hook.')
    return HttpResponse()

def validate_request(request):
    nonce = request.POST.get('nonce')
    key = request.POST.get('key')

    logger.debug('Validating response. Nonce: ' + nonce + '. Key: ' + key)

    h = hashlib.sha1()
    h.update(brewerydb.API_KEY + nonce)

    logger.debug('Result of sha1: ' + h.hexdigest())

    return h.hexdigest() == key

def fetch_beers(query):
    logger.debug('Querying Beer database with "{}"'.format(query))
    queryset = Beer.objects.filter(name__icontains=query)[:MAX_RESULTS]
    result = {}
    for beer in queryset:
        rating_queryset = Rating.objects.filter(beer__exact=beer.id)[:1]
        if not rating_queryset.count():
            logger.debug('No ratings found for {}.  Skipping'.format(beer.name))
            continue
        logger.debug('Adding "{}": "{}" to result.'.format(beer.id, beer.name))
        result[beer.id] = beer.name
    return result
