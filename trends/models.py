from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from beerdata.models import Beer, Brewery

BREWERY_DB_ID_LENGTH = 6
DECIMAL_FIELD_MAX_DIGITS = 4
DECIMAL_FIELD_DECIMAL_PLACES = 2

class Rating(models.Model):
    """
    Encapsulates a rating for a beer.
    """

    def __str__(self):
        return 'Beer {} rated {} on {}.'.format(self.beer.id, self.rating,
                self.date)

    # Fields
    # Use the default auto-incrementing key 'id'

    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS, 
            decimal_places=DECIMAL_FIELD_DECIMAL_PLACES)
    date = models.DateField()

