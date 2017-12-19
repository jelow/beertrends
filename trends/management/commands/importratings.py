import json, logging, fileinput

from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from trends.models import Rating
from beerdata.models import Beer, Brewery
from beerdata import brewerydb
from beerdata.update_beer import update_beer               
from beerdata.update_brewery import update_brewery

ARG_NAME = 'json_file'
URL_KEY = 'URL'
BEER_QUERY = 'beer'
BREWERY_QUERY = 'brewery'
KILL_SWITCH = 'KILL_'

logger = logging.getLogger('scraper.import')

class Command(BaseCommand):
    help = 'Imports ratings from JSON data'

    def add_arguments(self, parser):
        parser.add_argument(ARG_NAME)

    def handle(self, *args, **options):
        self.filename = options[ARG_NAME]

        try: 
            file = open(self.filename)
        except FileNotFoundError:
            return self.stdout.write(self.style.ERROR('File does not exist: ' + self.filename))
        except IOError as e:
            return self.stdout.write(self.style.ERROR('Error ' + e.errno + ' opening ' + self.filename))

        json_data = json.load(file)

        # Iterate through the breweries
        for brewery_key in json_data.keys():
            if brewery_key == URL_KEY:
                continue;
            elif brewery_key.startswith(KILL_SWITCH):
                continue


            logger.debug('Handling brewery ' + brewery_key)
            print('Handling brewery ' + brewery_key)
            
            self.current_string = brewery_key

            # Check if the brewery name already exists in the DB
            try:
                brewery = Brewery.objects.get(name=brewery_key)
                print('Found brewery in database.')
            except Brewery.DoesNotExist:
                print('Brewery not found in database.')

                brewery = self.search(BREWERY_QUERY, brewery_key)
                if brewery is None:
                    print('Brewery not found. Continuing.')
                    continue
            self.breweryId = brewery.id

            # Iterate through the brewery's beers
            for beer_key in json_data[brewery_key].keys():
                if beer_key == URL_KEY:
                    continue;
                elif beer_key.startswith(KILL_SWITCH):
                    continue

                self.current_string = beer_key

                logger.debug('Handling beer ' + beer_key)
                print('Handling beer ' + beer_key)

                # Check if the beer name already exists in the DB
                try:
                    beer = Beer.objects.get(name=beer_key)
                    print('Found beer in database.')
                except Beer.MultipleObjectsReturned:
                    continue
                except Beer.DoesNotExist:
                    print('Beer not found in database.')

                    beer = self.search(BEER_QUERY, beer_key)
                    if beer is None:
                        print('Beer not found. Continuing.')
                        continue

                ratings = json_data[brewery_key][beer_key]
                
                for date in ratings.keys():
                    if date == URL_KEY:
                        continue
                    try: 
                        self.create_rating(brewery, beer, date, ratings[date])
                    except:
                        continue

    def search(self, model, query):
        logger.debug('Searching {} database for {}'.format(model, query))
        
        if model is BREWERY_QUERY:
            queryset = Brewery.objects.filter(name__icontains=query)

            print('Found {} results in the database.'.format(queryset.count()))

            if queryset.count() is not 0:
                # Display options to user
                selection = self.select_option(queryset.values('id', 'name'), query)

                # If user didn't select an option, search BreweryDb
                if selection is None:
                    return self.search_brewerydb(BREWERY_QUERY, query)
                print('Found brewery in database.')
                self.update_json_file(queryset[selection].name)
                return queryset[selection]

            # If no results found, search BreweryDb
            else:
                return self.search_brewerydb(BREWERY_QUERY, query)

        elif model is BEER_QUERY:
            queryset = Beer.objects.filter(name__icontains=query)

            print('Found {} results in the database.'.format(queryset.count()))

            if queryset.count() is not 0:
                # Display options to user
                selection = self.select_option(queryset.values('id', 'name'),
                        query)

                # If user didn't select an option, search BreweryDb
                if selection is None:
                    return self.search_brewerydb(BEER_QUERY, query)
                print('Found beer in database.')
                self.update_json_file(queryset[selection].name)
                return queryset[selection]

            # If no results found, search BreweryDb
            else:
                return self.search_brewerydb(BEER_QUERY, query)

        else:
            raise ValueError('Incorrect model specified.')

    def search_brewerydb(self, model, query):
        MAX_RESULTS = 10
        print('Searching BreweryDb...')

        if model is BREWERY_QUERY:
            results = brewerydb.search(model, None, query)
        elif model is BEER_QUERY:
            results = brewerydb.search(model, self.breweryId, query)

        if results is None:
            print('No results found :(')
            return None

        print('Got {} results from BreweryDb.'.format(len(results)))

        if len(results) > MAX_RESULTS:
            print('Trimming to the top {} results'.format(MAX_RESULTS))
            results = results[:MAX_RESULTS]

        if len(results) == 0:
            self.update_json_file(KILL_SWITCH + self.current_string)
            return None

        selection = self.select_option(results, query)

        if selection is None:
            self.update_json_file(KILL_SWITCH + self.current_string)
            return None

        result = results[selection]

        if model is BREWERY_QUERY:
            brewery = brewerydb.query_brewery(result['id'])
            print('Adding {} to the database.'.format(result['name']))
            self.update_json_file(KILL_SWITCH + result['name'])
            return update_brewery(brewery)

        elif model is BEER_QUERY:
            beer = brewerydb.query_beer(result['id'])
            print('Adding {} to the database.'.format(result['name']))
            self.update_json_file(KILL_SWITCH + result['name'])
            return update_beer(beer, self.breweryId)

        else:
            raise ValueError('Incorrect model specified.')

    def select_option(self, option_list, query):
        logger.info('Displaying {} options to user.'.format(len(option_list)))

        counter = 0
        for option in option_list:
            print('{}: {}'.format(counter, option['name']))
            counter += 1

        while True:
            selection = input('Searching for: {}. (Hit enter if nothing matches): '.format(query))
            try:
                if selection is '':
                    return None
                selection = int(selection)
                option_list[selection]
                logger.debug('User input: {}'.format(selection))
                break
            except ValueError:
                self.stdout.write(self.style.ERROR('Enter an integer, dammit!'))
                logger.warn('The user is a dumbass.')
            except IndexError:
                # If none match
                if selection == counter:
                    logger.info('User selected "None of the above"')
                    return None

                self.stdout.write(self.style.ERROR('Selection out of range'))
                logger.warn('Selection out of range')

        logger.info('User selected {}'.format(option_list[selection]['name']))
        return selection

    def create_rating(self, brewery, beer, date_str, rating_str):
        ratingObj = Rating()

        ratingObj.beer = beer
        ratingObj.brewery = brewery

        ratingObj.date = self.parse_date(date_str)
        ratingObj.rating = self.parse_rating(rating_str)

        ratingObj.save()

    def parse_date(self, date_str):
        mask = '%b %d, %Y'
        return datetime.strptime(date_str, mask).date()

    def parse_rating(self, rating_str):
        if '/' in rating_str:
            return Decimal(rating_str[0])
        return Decimal(rating_str)

    def update_json_file(self, string):
        logger.info('Updating JSON file. Changing "{}" to "{}".'.format(self.current_string, string))

        with fileinput.FileInput(self.filename, inplace=True, backup='.bak') as file: 
            for line in file:
                print(line.replace('"' + self.current_string, '"' + string), end='')
