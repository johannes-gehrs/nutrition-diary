# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from datetime import datetime, date, timedelta
from collections import namedtuple
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_safe, require_http_methods
from app import scrape_fddb, models, forms


@require_safe
def index(request):
    if request.user.is_authenticated():
        return redirect('food_types')
    else:
        return redirect('login')


@require_safe
@login_required
def scrape(request, url):
    if not 'http://fddb.info/db/de/lebensmittel/' in url:
        return HttpResponse('This site is not supported, sorry.')

    ft = scrape_fddb.item(url)
    ft.timestamp = datetime.now()
    existing_fts = models.FoodType.objects.filter(source_url=url)
    if existing_fts:
        # Kind of a strange pattern, but this seems like the best way to achieve that some fields
        # are not updated.
        eft = existing_fts[0]
        ft.id, ft.timestamp, ft.serving_recent_quantity = \
            eft.id, eft.timestamp, eft.serving_recent_quantity
        ft.save()
    else:
        ft.save()
    return redirect(reverse('food_type', kwargs={'id': ft.id}))


@require_safe
@login_required
def food_types(request):
    fts = models.FoodType.objects.all().order_by('-timestamp')
    return render(request, 'food_types.html',
                  {'fts': fts, 'form': forms.ServingsEaten(initial={'next': 'food_types'})})


def _add_serving_message(quantity, name):
    if quantity != 1:
        serving = 'Portionen'
    else:
        serving = 'Portion'
    return 'Du hast {0} {1} {2} hinzugefügt.'.format(unicode(quantity), serving, name)


@require_http_methods(['GET', 'POST'])
@login_required
def food_type(request, id):
    ft = get_object_or_404(models.FoodType, id=id)

    if request.method == 'POST':
        bound_form = forms.ServingsEaten(request.POST)
        if bound_form.is_valid():

            date_choice = bound_form.cleaned_data['date']
            if date_choice == 'yesterday':
                date_of_consumption = (date.today() - timedelta(days=1))
            elif date_choice == 'today':
                date_of_consumption = (date.today())
            elif date_choice == 'tomorrow':
                date_of_consumption = (date.today() + timedelta(days=1))

            serving = models.Serving(user=request.user,
                                     food_type=ft,
                                     date_of_consumption=date_of_consumption,
                                     quantity=int(
                                         bound_form.cleaned_data['quantity']) * ft.serving_size)
            ft.timestamp, ft.serving_recent_quantity = \
                datetime.now(), bound_form.cleaned_data['quantity']
            ft.save()
            serving.save()
            messages.add_message(request, messages.SUCCESS,
                                 _add_serving_message(int(bound_form.cleaned_data['quantity']),
                                                      ft.name))
            next = bound_form.cleaned_data['next']
            return redirect(next)
        else:
            form = bound_form
    else:
        form = forms.ServingsEaten(initial={'quantity': ft.serving_recent_quantity})

    return render(request, 'food_type.html',
                  {'ft': ft,
                   'serving': ft.values(),
                   'serving_points': ft.points(quantity=ft.serving_size),
                   'form': form})


@require_http_methods(['GET', 'POST'])
@login_required
def edit_ft_serving(request, id):
    ft = get_object_or_404(models.FoodType, id=id)

    if request.method == 'POST':
        bound_form = forms.ServingMaster(request.POST)
        if bound_form.is_valid():
            ft.serving_description = bound_form.cleaned_data['description']
            ft.serving_size = bound_form.cleaned_data['quantity']
            ft.save()
            return redirect((reverse('food_type', kwargs={'id': ft.id})))
        else:
            form = bound_form
    else:
        form = forms.ServingMaster(initial={'quantity': ft.serving_size,
                                            'description': ft.serving_description})

    return render(request, 'serving_edit.html', {'ft': ft, 'form': form})


@login_required
def diary(request):
    servings_grouped_by_day = []
    Day = namedtuple('Day', ['servings', 'sum'])
    serving_dates_list_of_dicts = models.Serving.objects.filter(user=request.user).order_by(
        '-date_of_consumption').distinct().values('date_of_consumption')[:30]
    serving_dates = [item['date_of_consumption'] for item in serving_dates_list_of_dicts]

    for serving_date in serving_dates:
        servings = models.Serving.objects \
            .filter(user=request.user, date_of_consumption=serving_date) \
            .order_by('timestamp')
        sum_of_points = sum([serving.points() for serving in servings])
        servings_grouped_by_day.append((serving_date, Day(servings, sum_of_points)))

    return render(request, 'diary.html', {"days": servings_grouped_by_day})


@require_http_methods(['DELETE'])
@login_required()
def delete_serving(request, id):
    serving = get_object_or_404(models.Serving, user=request.user, id=id)
    serving.delete()
    return HttpResponse('Serving deleted!')
