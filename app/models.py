# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from decimal import Decimal, ROUND_HALF_DOWN
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class FoodType(models.Model):
    BASE_SIZE_GRAMS = Decimal(100)

    source_url = models.URLField("Ursprungs-URL", unique=True)
    name = models.CharField("Name", max_length=80)
    calories = models.PositiveIntegerField("Kalorien")
    protein = models.DecimalField("Protein in g", decimal_places=1, max_digits=3)
    carbon = models.DecimalField("Kohlenhydrate in g", decimal_places=1, max_digits=3)
    fat = models.DecimalField("Fett in g", decimal_places=1, max_digits=3)
    fiber = models.DecimalField("Carbon Fiber in g", decimal_places=1, max_digits=3)
    serving_description = models.CharField("Beschreibung der Portion", max_length=80)
    serving_size = models.DecimalField("Portionsgröße in g", decimal_places=1, max_digits=5)
    timestamp = models.DateTimeField("Zeitpunkt der letzten Verwendung")
    serving_recent_quantity = models.PositiveIntegerField("Zuletzt verwendete Menge", default=1)

    def __uncode__(self):
        return self.name

    def _lesser_of_fiber_or_4(self):
        if self.fiber > 4:
            return Decimal(4)
        else:
            return self.fiber

    def _round_points(self, points):
        return points.quantize(Decimal('1.'), rounding=ROUND_HALF_DOWN)

    def points(self, rounded=True, quantity=None):
        points_base = (Decimal(self.calories) / Decimal(50)) + (self.fat / Decimal(12)) \
                      - (self._lesser_of_fiber_or_4() / 5)

        if quantity is not None:
            points = (points_base * (quantity / self.BASE_SIZE_GRAMS))
        else:
            points = points_base

        if rounded:
            return self._round_points(points)
        else:
            return points

    def values(self, quantity=None, keys=None):
        if quantity is None:
            quantity = self.serving_size

        adjust = lambda my_value: my_value * (quantity / self.BASE_SIZE_GRAMS)
        base_keys = ['calories', 'protein', 'carbon', 'fat', 'fiber']
        values = [eval('self.' + key) for key in base_keys]

        adjusted = [adjust(value) for value in values]
        zipped = zip (base_keys, adjusted)
        complete_dict = {item[0]: item[1] for item in zipped}

        if keys is not None:
            return {key: item[key] for item in complete_dict}
        else:
            return complete_dict


class Serving(models.Model):
    timestamp = models.DateTimeField("Zeitpunkt der Eintragung des Verzehrs",
                                     default=datetime.now())
    date_of_consumption = models.DateField("Tag des Verzehrs")
    user = models.ForeignKey(User, related_name='serving_set')
    food_type = models.ForeignKey(FoodType)
    quantity = models.DecimalField("Menge in g", decimal_places=0, max_digits=5)

    def points(self, rounded=True):
        return self.food_type.points(quantity=self.quantity, rounded=rounded)


class Dieter(models.Model):
    user = models.OneToOneField(User)
    budget = models.PositiveIntegerField("Punktebudget pro Tag")
