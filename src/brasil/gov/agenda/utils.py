# -*- coding: utf-8 -*-

from DateTime import DateTime
from datetime import date
from datetime import datetime
from datetime import timedelta
from zope.i18nmessageid import MessageFactory


PloneMessageFactory = MessageFactory('plonelocales')


def weekday_abbr(date):
    return date.strftime('%a').lower()


def month_abbr(date):
    return date.strftime('%b').lower()


def translate_weekday(date):
    weekday = 'weekday_%s' % weekday_abbr(date)
    return PloneMessageFactory(weekday)


def translate_month(date):
    month = 'month_%s' % month_abbr(date)
    return PloneMessageFactory(month)


def format_date(date):
    parts = {}
    parts['weekday'] = translate_weekday(date)
    parts['day'] = date.strftime('%d')
    parts['month'] = translate_month(date)
    parts['year'] = date.strftime('%Y')
    return '%(weekday)s, %(day)s de %(month)s de %(year)s' % parts


def rfc2445dt(value):
    if isinstance(value, datetime):
        value = DateTime(value.strftime('%Y/%m/%d %H:%M'))
    # return UTC in RFC2445 format YYYYMMDDTHHMMSSZ
    return value.HTML4().replace('-', '').replace(':', '')


def tomorrow():
    """ Return datetime.date for tomorrow """
    return date.today() + timedelta(1)
