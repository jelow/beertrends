from django.core.management.base import BaseCommand, CommandError

import beerdata.brewerydb as brewerydb
from beerdata.models import Beer, Brewery
from beerdata.update_beer import update_beer

class Command(BaseCommand):
    help = 'Adds body to beers in the database'

    def handle(self, *args, **options):
        breweries = Brewery.objects.all().values('id')

        for brewery in breweries:
            self.stdout.write(self.style.SUCCESS('Brewery ' + brewery['id']))
            beers = brewerydb.query_brewery_beers(brewery['id'])

            for beer in beers:
                self.stdout.write(self.style.SUCCESS('Beer ' + beer['id']))
                update_beer(beer, None, True)

        self.stdout.write(self.style.SUCCESS('Done'))
