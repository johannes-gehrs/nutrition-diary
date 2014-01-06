# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from django.contrib import admin
from app import models


class FoodTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'points')


admin.site.register(models.FoodType, FoodTypeAdmin)
admin.site.register(models.Serving)
admin.site.register(models.Dieter)
