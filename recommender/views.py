import logging
import random
import re

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from .models import *
from beerdata import brewerydb
from beerdata.update_beer import update_beer
from beerdata.update_brewery import update_brewery, add_brewery_beers
from beerdata.models import Beer, Brewery
from . import opennorth
from userprofile.models import UserProfile

logger = logging.getLogger('recommender.views')

ABV_CONST = 131.25

def recommender(request):
    return render(request, 'recommender/recommender.html', {})

def make_recommendation(request):
    logger.info('Starting recommendation.')
    logger.debug(request.POST)

    r = Recommendation()

    r.ibu = int(request.POST.get('ibu'))
    r.abv = float(request.POST.get('abv'))
    r.srm = int(request.POST.get('srm'))
    r.og, r.fg = calculate_og_and_fg(float(request.POST.get('body')), r.abv)
    r.fuzziness = float(request.POST.get('fuzz'))
    r.save()

    logger.debug('Generated recommendation: ' + r.__str__())

    # Load nearby breweries and their beers into the database
    lat, lng = get_location(request)
    dist = int(request.POST.get('distance'))

    breweries = brewerydb.query_nearby_breweries(lat, lng, dist)
    seedDatabase(breweries)

    beers = find_beers(r, breweries)
    r.beers = beers
    r.save()

    saved_beers = get_saved_beers(beers, request)
    watched_breweries = get_watched_breweries(breweries, request)

    logger.debug('saved_beers: ' + str(saved_beers))
    logger.debug('watched_breweries: ' + str(watched_breweries))
    logger.debug('Rendering result.')
    return render(request, 'recommender/result.html', create_context(request, r.beers, saved_beers, watched_breweries))

def seedDatabase(breweries):
    logger.debug('Seeding database')

    for brewery in breweries:
        # Add the brewery. Continue if it already exists in the database
        info = {'id': brewery['brewery']['id'], 'name':
                brewery['brewery']['name'], 'latitude': brewery['latitude'],
                'longitude': brewery['longitude']}
        try:
            if update_brewery(info):
                add_brewery_beers(brewery['brewery']['id'])
        except ValueError:
            continue;


def calculate_og_and_fg(body, abv):
    # Map body to FG
    fg = ((Beer.FG_MAX - Beer.FG_MIN) * body) + Beer.FG_MIN

    # Calculate OG
    og = (abv / ABV_CONST) + fg

    return (og, fg)

def find_beers(r, breweries):
    """Finds beers that match the specifications in the
    provided Recommendation, and associates them with it.

    Args: r             - Recommendation object without associated beers
          breweries     - A list of eligible breweries
    Returns: A QuerySet of the matching beers
    """

    logger.debug('Finding beer recommendations.')

    # Extract the brewery IDs
    brewery_ids = []
    for brewery in breweries:
        brewery_ids.append(brewery['brewery']['id'])

    # Calculate the search range of each attribute
    ibu_min, ibu_max = calculate_fuzzy_values(r.ibu, Beer.IBU_MIN, Beer.IBU_MAX, r.fuzziness)
    abv_min, abv_max = calculate_fuzzy_values(r.abv, Beer.ABV_MIN, Beer.ABV_MAX, r.fuzziness)
    og_min, og_max = calculate_fuzzy_values(r.og, Beer.OG_MIN, Beer.OG_MAX, r.fuzziness)
    fg_min, fg_max = calculate_fuzzy_values(r.fg, Beer.FG_MIN, Beer.FG_MAX, r.fuzziness)
    srm_min, srm_max = calculate_fuzzy_values(r.srm, Beer.SRM_MIN, Beer.SRM_MAX, r.fuzziness)

    beers = Beer.objects.filter(brewery__in = brewery_ids)
    beers = beers.filter(ibu__range = (ibu_min, ibu_max))
    beers = beers.filter(abv__range = (abv_min, abv_max))
    beers = beers.filter(srm__range = (srm_min, srm_max))
    beers = beers.filter(og__range = (og_min, og_max))
    beers = beers.filter(fg__range = (fg_min, fg_max))

    logger.debug('Found ' + str(beers.count()) + ' beers.')

    return beers

def calculate_fuzzy_values(value, min_value, max_value, fuzziness):
    value_range = (max_value - min_value) * fuzziness

    tmp_min = value - value_range
    tmp_max = value + value_range

    fuzzy_min = min_value if tmp_min < min_value else tmp_min
    fuzzy_max = max_value if tmp_max > max_value else tmp_max

    return (fuzzy_min, fuzzy_max)

def create_context(request, beers, saved_beers, watched_breweries):
    context = {
        'default': {
            'ibu': request.POST.get('ibu'),
            'abv': request.POST.get('abv'),
            'srm': request.POST.get('srm'),
            'body': request.POST.get('body'),
            'distance': request.POST.get('distance'),
        }
    }

    context['beers'] = beers.all()
    context['saved_beers'] = saved_beers
    context['watched_breweries'] = watched_breweries

    logger.debug('Context: ' + str(context))
    return context

def get_location(request):
    logger.debug('Getting location data.')
    try:
        lat = request.POST.get('userLat')
        lng = request.POST.get('userLong')

        if lat is '' or lng is '':
            logger.debug('Empty location data.')
            raise KeyError

    except KeyError:
        logger.debug('No location data found. Falling back to API query.')
        try: 
            postcode = sanitizePostcode(request.POST.get('postcode'))
        except ValueError:
            logger.debug('Postcal code format error')
            error = {'message': 'Postal code format error'}
            return render(request, 'recommender/error.html', error)

        latLng = opennorth.query_postcode(postcode)
        lat = latLng['lat']
        lng = latLng['lng']

    logger.debug('Got location data. ' + str(lat) + ', ' + str(lng))
    return (lat, lng)

def sanitizePostcode(postcode):
    logger.debug('Sanitizing postcode ' + postcode)

    # Remove whitespace and capitalize letters
    postcode = postcode.replace(' ', '')
    postcode = postcode.upper()

    # Validate format
    logger.debug('Checking postcode ' + postcode)
    r = re.compile('[A-Z]\d[A-Z]\d[A-Z]\d')
    if r.match(postcode) is None:
        raise ValueError('Invalid postal code format')
    return postcode

def get_watched_breweries(breweries, request):
    watched_breweries = []
    if not request.user.is_authenticated():
        return watched_breweries

    user = UserProfile.objects.get(user__username=request.user.username)
    brewery_id_list = [brewery['brewery']['id'] for brewery in breweries]
    logger.debug('brewery_id_list: ' + str(brewery_id_list))

    logger.debug('watchlist.all: ' + str(user.brewery_watchlist.all().values('id')))
    for brewery in user.brewery_watchlist.all().values('id'):
        if brewery['id'] in brewery_id_list:
            watched_breweries.append(brewery['id'])
    return watched_breweries

def get_saved_beers(beers, request):
    saved_beers = []
    if not request.user.is_authenticated():
        return saved_beers
    user = UserProfile.objects.get(user__username=request.user.username)
    beer_id_list = list(beers.values('id'))
    beer_ids = []
    for d in beer_id_list:
        beer_ids.append(d['id'])
    for beer in user.beer_wishlist.all().values('id'):
        if beer['id'] in beer_ids:
            saved_beers.append(beer['id'])
    return saved_beers

