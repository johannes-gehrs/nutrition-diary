# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from decimal import Decimal
import datetime
from factory import Sequence, PostGenerationMethodCall
from factory.django import DjangoModelFactory
from django.contrib.auth import models as auth_models
from app import models

MYPASSWORD = 'wordpass'


class AdminUserFactory(DjangoModelFactory):
    FACTORY_FOR = auth_models.User

    username = Sequence(lambda n: 'joe_admin%d' % n)
    first_name = u'Joe'
    last_name = u'Admin'
    email = u'admin@example.com'
    is_staff = True
    is_superuser = True
    password = PostGenerationMethodCall('set_password', MYPASSWORD)


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = auth_models.User

    username = Sequence(lambda n: 'josh_user%d' % n)
    first_name = u'Josh'
    last_name = u'User'
    email = u'user@example.com'
    password = PostGenerationMethodCall('set_password', MYPASSWORD)


class FoodTypeFactory(DjangoModelFactory):
    FACTORY_FOR = models.FoodType

    name = "Körniger Frischkäse"
    source_url = Sequence(lambda  n: "http://fddb.info/db/de/lebensmittel/" \
                 "gut_und_guenstig_koerniger_frischkaese_3580%d/index.html" % n)
    calories = 98
    protein = Decimal('12.5')
    carbon = Decimal('3')
    fat = Decimal('4')
    fiber = Decimal('0')
    serving_description = '1 Aufstrich (30 g)'
    serving_size = Decimal('30')
    timestamp = datetime.datetime.now()
    serving_recent_quantity = 1


class ServingFactory(DjangoModelFactory):
    FACTORY_FOR = models.Serving

    timestamp = datetime.datetime.now()
    date_of_consumption = datetime.date(2014, 3, 11)
    user = UserFactory()
    food_type = FoodTypeFactory()
    quantity = Decimal('30')
