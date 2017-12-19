from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from beerdata.models import Beer

DECIMAL_FIELD_MAX_DIGITS = 4
DECIMAL_FIELD_DECIMAL_PLACES = 2

class Recommendation(models.Model):

    FUZZ_MIN = 0.0
    FUZZ_MAX = 1.0

    DEFAULT_FUZZINESS = 0.1

    def __str__(self):
        return 'Recommendation {}. ibu: {}. abv: {}. og: {}. fg: {}. fuzz: {}.'.format(self.id, self.ibu, self.abv, self.og, self.fg, self.fuzziness)

    ibu = models.PositiveSmallIntegerField(
            validators = [
                MinValueValidator(Beer.IBU_MIN),
                MaxValueValidator(Beer.IBU_MAX)])
    
    abv = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,
            decimal_places=DECIMAL_FIELD_DECIMAL_PLACES,
            validators = [
                MinValueValidator(Beer.ABV_MIN),
                MaxValueValidator(Beer.ABV_MAX)])

    srm = models.PositiveSmallIntegerField(
            validators = [
                MinValueValidator(Beer.SRM_MIN),
                MaxValueValidator(Beer.SRM_MAX)])

    og = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,
            decimal_places=DECIMAL_FIELD_DECIMAL_PLACES,
            validators = [
                MinValueValidator(Beer.OG_MIN),
                MaxValueValidator(Beer.OG_MAX)])

    fg = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,
            decimal_places=DECIMAL_FIELD_DECIMAL_PLACES,
            validators = [
                MinValueValidator(Beer.FG_MIN),
                MaxValueValidator(Beer.FG_MAX)])

    fuzziness = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,
            decimal_places=DECIMAL_FIELD_DECIMAL_PLACES,
            default=Decimal(DEFAULT_FUZZINESS),
            validators = [
                MinValueValidator(FUZZ_MIN),
                MaxValueValidator(FUZZ_MAX)])

    beers = models.ManyToManyField(Beer)

