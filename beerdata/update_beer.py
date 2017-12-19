import logging
import random
from .models import Beer, Brewery
from . import brewerydb

ABV_CONST = 131.25

logger = logging.getLogger('beerdata.update_beer')

def update_beer(beer, breweryId=None, update=False):
    """
    Adds or updates a beer in the database.

    Params:
    beer        - a dictionary of beer data from BreweryDb
    breweryId   - If None, don't mess with the brewery
    update      - If false, abort if beer already exists in the database
    """

    logger.info('Adding beer ' + beer['id'] + ' to the database.')

    bId = beer['id']

    # Store the style info, in case it's needed to fake values
    # If there's no style info, fuck it we out
    try:
        style = brewerydb.query_style(beer['styleId'])
    except KeyError:
        logger.warn('No style data. Aborting.')
        return

    try:
        beerObj = Beer.objects.get(id=bId)
        if update:
            logger.info('Updating beer ' + bId)
        else:
            logger.info('Beer already exists in database. Aborting.')
            return
    except Beer.DoesNotExist:
        if update:
            logger.warn('Beer ' + bId + ' does not exist in database; cannot update. Aborting.')
            return
        else:
            logger.info('Beer does not exist in database. Adding new entry.')
            beerObj = Beer()

    beerObj.id = beer['id']

    try: beerObj.name = beer['name']
    except KeyError: logger.warn('\'name\' key does not exist.')

    try: beerObj.desc = beer['description']
    except KeyError: logger.warn('\'description\' key does not exist.')

    try: beerObj.ibu = int(beer['ibu'])
    except KeyError: 
        logger.warn('\'ibu\' key does not exist.')
        beerObj.ibu = generate_fake_value(style, 'ibu')

    try: beerObj.abv = beer['abv']
    except KeyError: 
        logger.warn('\'abv\' key does not exist.')
        beerObj.abv = generate_fake_value(style, 'abv')

    try: beerObj.og = beer['originalGravity']
    except KeyError: 
        logger.warn('\'originalGravity\' key does not exist.')
        beerObj.og = generate_fake_value(style, 'og')

    try: beerObj.srm = int(beer['srmId'])
    except KeyError: 
        logger.warn('\'srm\' key does not exist.')
        beerObj.srm = generate_fake_value(style, 'srm')

    try: 
        beerObj.label = beer['labels']['large']
    except KeyError: 
        logger.warn('\'labels.large\' key does not exist. Falling back to medium.')
        try:
            beerObj.label = beer['labels']['medium']
        except KeyError: 
            logger.warn('\'labels.medium\' key does not exist.')

    try: 
        beerObj.fg = calculate_fg(float(beerObj.abv), float(beerObj.og))
        beerObj.body = calculate_body(float(beerObj.fg))
    except TypeError: 
        logger.warn('Cannot calculate final gravity or body due to missing data.')

    # Add it to the brewery and save
    if breweryId: 
        beerObj.brewery = Brewery.objects.get(pk = breweryId)
    beerObj.save()

    return beerObj

def calculate_fg(abv, og):
    fg = og - (abv / ABV_CONST)
    return Beer.FG_MIN if fg < Beer.FG_MIN else fg
    
def calculate_body(fg):
    body = (fg - Beer.FG_MIN) / (Beer.FG_MAX - Beer.FG_MIN)
    if body > 1.0: return 1.0
    return 0.0 if body < 0.0 else body

def generate_fake_value(style, field):
    logger.info('Generating fake value for ' + field)

    if field is 'ibu':
        try:
            return random.randint(int(style['ibuMin']), int(style['ibuMax']))
        except KeyError:
            return random.randint(Beer.IBU_MIN, Beer.IBU_MAX)

    if field is 'srm':
        try:
            return random.randint(int(style['srmMin']), int(style['srmMax']))
        except KeyError:
            return random.randint(Beer.SRM_MIN, Beer.SRM_MAX)

    if field is 'og':
        try:
            return random.uniform(float(style['ogMin']), float(style['ogMax']))
        except KeyError:
            return random.uniform(Beer.OG_MIN, Beer.OG_MAX)

    if field is 'abv':
        try:
            return random.uniform(float(style['abvMin']), float(style['abvMax']))
        except KeyError:
            return random.uniform(Beer.ABV_MIN, Beer.ABV_MAX)
