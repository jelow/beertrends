import logging
import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import *
from beerdata.models import Beer, Brewery

logger = logging.getLogger('trends.views')

def trends(request):
    if request.method == 'POST':
        if not request.POST:
            logger.info('Empty POST data. Returning default context.')
            return render(request, 'trends/trends.html', {})

    beer_id = request.POST.get('beer_id')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    
    if not start_date:
        start_date = datetime.datetime.fromtimestamp(0).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')

    try:
        validate_date(start_date)
        validate_date(end_date)
    except ValueError as e:
        return render(request, 'trends/trends.html', error_context(str(e)))

    if start_date > end_date:
        return render(request, 'trends/trends.html', error_context('Start date is after end date.'))

    logger.debug('start date: ' + start_date)
    logger.debug('end date: ' + end_date)

    if not beer_id:
        logger.info('No beer id supplied. Returning default context.')
        return render(request, 'trends/trends.html', {})

    try:
        ratings_dict = fetch_ratings(beer_id, start_date, end_date)
    except Exception as e:
        return render(request, 'trends/trends.html', error_context(str(e)))
    
    return render(request, 'trends/trends.html', build_context(beer_id, ratings_dict))

def fetch_ratings(beer_id, start_date, end_date):
    logger.info('Fetching ratings for {} from {} to {}'.format(beer_id, start_date, end_date))

    ratings_queryset = Rating.objects.filter(beer__exact = beer_id)
    ratings_queryset = ratings_queryset.filter(date__range = [start_date, end_date])

    if len(ratings_queryset) is 0:
        logger.warn('No ratings found for ID ' + beer_id)
        raise Rating.DoesNotExist('No ratings found')

    ratings = {}
    for rating in ratings_queryset:
        logger.debug('Adding rating: "{}"'.format(str(rating)))
        ratings[rating.date] = rating.rating

    return ratings

def error_context(message):
    context = { "status": "error", "message": message }
    logger.debug('Created error context: ' + str(context))
    return context

def build_context(beer_id, ratings_dict):
    context = { "status": "success" }
    context['ratings'] = { beer_id: ratings_dict }
    logger.debug('Created context: ' + str(context))
    return context

def validate_date(date_string):
    logger.debug('Validating date: ' + date_string)

    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
