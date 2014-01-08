# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from django import forms
from django.contrib.auth.forms import AuthenticationForm


widget_attrs = {'class': 'form-control'}


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs=widget_attrs),
                           label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs=widget_attrs),
                               label="Passwort")


class ServingsEaten(forms.Form):
    CHOICES = (('yesterday', 'gestern'), ('today', 'heute'), ('tomorrow', 'morgen'))

    quantity = forms.IntegerField(widget=forms.NumberInput(attrs=widget_attrs), label="Anzahl",
                                  initial=1, min_value=1, max_value=25)
    date = forms.ChoiceField(widget=forms.Select(attrs=widget_attrs), label="Zeitpunkt",
                             initial='today', choices=CHOICES)
    next = forms.CharField(widget=forms.HiddenInput, initial='diary')


class ServingMaster(forms.Form):
    description = forms.CharField(widget=forms.TextInput(attrs=widget_attrs), label="Beschreibung")
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs=widget_attrs), min_value=1,
                                  max_value=2000, label='Menge in g')
