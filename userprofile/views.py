import logging

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import *
from beerdata.models import Beer, Brewery

logger = logging.getLogger('userprofile.views')

@login_required
def profile(request):
    profile = request.user.profile
    context = get_context(profile)
    return render(request, 'userprofile/userprofile.html', context)

@login_required
def add_beer_to_wishlist(request, beer_id):
    logger.info('Adding beer to wishlist: ' + beer_id)
    profile = request.user.profile
    beer = get_object_or_404(Beer, id=beer_id)
    profile.beer_wishlist.add(beer)

    return HttpResponse(status=201)

@login_required
def remove_beer_from_wishlist(request, beer_id):
    logger.info('Removing beer to wishlist: ' + beer_id)
    profile = request.user.profile
    beer = get_object_or_404(Beer, id=beer_id)
    profile.beer_wishlist.remove(beer)

    context = get_context(profile)
    return render(request, 'userprofile/userprofile.html')

@login_required
def add_brewery_to_watchlist(request, brewery_id):
    logger.info('Adding brewery to watchlist: ' + brewery_id)
    profile = request.user.profile
    brewery = get_object_or_404(Brewery, id=brewery_id)
    profile.brewery_watchlist.add(brewery)

    return HttpResponse(status=201)

@login_required
def remove_brewery_from_watchlist(request, brewery_id):
    profile = request.user.profile
    brewery = get_object_or_404(Brewery, id=brewery_id)
    profile.brewery_watchlist.remove(brewery)

    context = get_context(profile)
    return render(request, 'userprofile/userprofile.html', context)

@login_required
def dismiss_notification(request, notification_id):
    profile = request.user.profile
    notification = get_object_or_404(Notification, pk=notification_id)
    notification.delete()

    context = get_context(profile)
    return render(request, 'userprofile/userprofile.html', context)

def get_context(profile):
    my_beers = profile.beer_wishlist.values()
    my_breweries = profile.brewery_watchlist.values()

    # Get notifications
    notifications = []
    notifications = Notification.objects.filter(user__user__username=profile.user.username).values()
    for note in notifications:
        beer = Beer.objects.get(pk=note['beer_id'])
        brewery = Brewery.objects.get(pk=note['brewery_id'])
        note['beer_name'] = beer.name
        note['brewery_name'] = brewery.name
    context = {
        'beer_id_list' : [beer['id'] for beer in my_beers],
        'beer_list' : my_beers,
        'brewery_list' : my_breweries,
        'notifications' : notifications
    }
    logger.debug(str(context))
    return context
