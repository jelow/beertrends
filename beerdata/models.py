from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

CHAR_FIELD_MAX_LENGTH = 256
DECIMAL_FIELD_MAX_DIGITS = 4
DECIMAL_FIELD_DECIMAL_PLACES = 2

class Brewery(models.Model):
    """
    A wrapper for a BreweryDb brewery.
    """

    def __str__(self):
        return self.name

    # Fields
    id = models.CharField(primary_key=True, editable=False, 
            max_length=CHAR_FIELD_MAX_LENGTH)
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    lat = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    lng = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)

class Beer(models.Model):
    """
    A wrapper for a BreweryDb beer.
    """
    IBU_MIN = 0
    IBU_MAX = 100

    ABV_MIN = 0
    ABV_MAX = 18

    SRM_MIN = 0
    SRM_MAX = 50

    # OG and FG values are from https://www.brewersfriend.com/2009/02/04/beer-styles-original-gravity-and-final-gravity-chart/
    OG_MIN = 1.020
    OG_MAX = 1.130

    FG_MIN = 1.0
    FG_MAX = 1.040 

    BODY_MIN = 0.0
    BODY_MAX = 1.0


    def __str__(self):
        return self.name

    # Fields
    id = models.CharField(primary_key=True, editable=False, 
            max_length=CHAR_FIELD_MAX_LENGTH)
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    desc = models.TextField(null=True)
    ibu = models.PositiveSmallIntegerField(null=True)
    abv = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS, 
            decimal_places=DECIMAL_FIELD_DECIMAL_PLACES, null=True)
    srm = models.PositiveSmallIntegerField(null=True)
    og = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,
            decimal_places=DECIMAL_FIELD_DECIMAL_PLACES, null=True)
    fg = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,
            decimal_places=DECIMAL_FIELD_DECIMAL_PLACES, null=True)
    body = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,
            decimal_places=DECIMAL_FIELD_DECIMAL_PLACES, null=True)
    label = models.URLField(null=True)

    # Many-to-one relationship with breweries
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
