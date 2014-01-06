# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from datetime import date
from app import models

def points_today(request):
    if request.user.is_authenticated():
        servings = models.Serving.objects.filter(user=request.user, date_of_consumption=date.today())
        sum_of_points = sum([serving.points() for serving in servings])
        return {'todays_points': sum_of_points}
    else:
        return {'todays_points': None}
