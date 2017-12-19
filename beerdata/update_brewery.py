import logging
from .models import Beer, Brewery
from . import brewerydb
from . import update_beer

from userprofile.models import UserProfile, Notification

logger = logging.getLogger('beerdata.update_brewery')

def update_brewery(brewery, update=False):
    """
    Adds or updates a brewery in the database.

    Params:
    brewery - a dictionary of brewery data from BreweryDb
    update  - If false, abort if brewery already exists in the database
    """

    bId = brewery['id']

    try:
        breweryObj = Brewery.objects.get(id=bId)
        if update:
            logger.info('Updating brewery ' + bId)
        else:
            logger.info('Brewery already exists in database. Aborting.')
            return None
    except Brewery.DoesNotExist:
        if update:
            logger.warn('Brewery ' + bId + ' does not exist in database; cannot update. Aborting.')
            return None
        else:
            logger.info('Brewery does not exist in database. Adding new entry.')
            breweryObj = Brewery()

    # Create and save the new Brewery object
    breweryObj.id = bId
    breweryObj.name = brewery['name']
    breweryObj.lat = brewery['latitude']
    breweryObj.lng = brewery['longitude']
    breweryObj.save()

    return breweryObj

def add_brewery_beers(breweryId):
    beers = brewerydb.query_brewery_beers(breweryId)
    for beer in beers:
        update_beer.update_beer(beer, breweryId)

def new_beer(beerId, breweryId):
    users = UserProfile.objects.filter(brewery_watchlist__id__exact=breweryId)
    logger.info('Alerting {} users of new beer {} at brewery {}'.format(str(users.count()), beerId, breweryId))
    for user in users:
        logger.info('Alerting user ' + user.username)
        notification = Notification()
        notification.seen = False
        notification.beer = Beer.objects.get(pk=beerId)
        notification.brewery = Brewery.objects.get(pk=breweryId)
        notification.user = user
        notification.save()
