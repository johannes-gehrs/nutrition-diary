# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from decimal import Decimal
import re
from pyquery import PyQuery as Pq
from app import models


def _decimal_from_string(value_string):
    decimal_match = re.search(r'\d+\,\d+', value_string)
    if decimal_match is not None:
        return Decimal(decimal_match.group().replace(',', '.'))
    else:
        return Decimal(re.search(r'\d+', value_string).group())


def _quantities(pq_page):
    identifier_divs = pq_page('div.sidrow')
    raw_values = {Pq(div).text(): Pq(div).next().text() for div in identifier_divs}
    relevant_keys = ['Fett', 'Ballaststoffe', 'Kohlenhydrate', 'Protein', 'Kalorien']
    filtered_values = {key: raw_values.get(key, '0 g') for key in relevant_keys}
    return {key: _decimal_from_string(filtered_values[key]) for key in filtered_values}


def _serving(pq_page):
    serving = pq_page('a.servb')[0]
    description = serving.text_content()
    serving_size_in_g_match = re.search(r'\d+\ g', description)
    serving_size_in_ml_match = re.search(r'\d+\ ml', description)

    to_int = lambda string: int(re.search(r'\d+', string).group())

    if serving_size_in_g_match is not None:
        serving_size_in_g_as_int = to_int(serving_size_in_g_match.group())
    # We simply treat ml as grams (Punk rock)
    elif serving_size_in_ml_match is not None:
        serving_size_in_g_as_int = to_int(serving_size_in_ml_match.group())
    else:
        raise ValueError("Can't find serving size")

    return description, serving_size_in_g_as_int


def _name(pq_page):
    return pq_page('div.pageheadline h1').text()


def item(url):
    pq_page = Pq(url)

    name = _name(pq_page)
    quantities = _quantities(pq_page)
    serving = _serving(pq_page)

    return models.FoodType(name=name,
                           source_url=url,
                           calories=quantities['Kalorien'],
                           fiber=quantities['Ballaststoffe'],
                           fat=quantities['Fett'],
                           carbon=quantities['Kohlenhydrate'],
                           protein=quantities['Protein'],
                           serving_description=serving[0],
                           serving_size=serving[1])
