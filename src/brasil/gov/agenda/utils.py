# -*- coding: utf-8 -*-
from six.moves import range  # noqa: I001
from DateTime import DateTime
from datetime import date
from datetime import datetime
from datetime import timedelta
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
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


class AgendaMixin:

    """Common methods and functions used by views and and tiles."""

    def _translate(self, msgid, locale='plonelocales', mapping=None):
        tool = getToolByName(self.context, 'translation_service')
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        current_language = portal_state.language()
        # XXX: Por que é retornado 'pt-br' do portal_state ao invés de 'pt_BR'?
        # Quando uso 'pt-br' ao invés de 'pt_BR', não pega a tradução quando
        # feita de forma manual.
        target_language = ('pt_BR' if current_language == 'pt-br'
                           else self.current_language)
        return tool.translate(msgid,
                              locale,
                              mapping=mapping,
                              context=self.context,
                              target_language=target_language)

    def month(self):
        tool = getToolByName(self.context, 'translation_service')
        today = datetime.now()
        strmonth = self._translate(tool.month_msgid(today.strftime('%m')))
        return {
            'strmonth': strmonth[:3].upper(),
            'strmonthcomplete': strmonth.upper(),
            'month': today.month,
            'year': today.year,
        }

    def days(self):
        tool = getToolByName(self.context, 'translation_service')
        today = datetime.now()
        # get a list with 3 days before and 3 days after today
        days = [(today + timedelta(i)) for i in range(-3, 4)]
        weekdays = []
        for day in days:
            cssclass = ['day']
            if day == today:
                cssclass.append('is-selected')
            if self.agenda.get(day.strftime('%Y-%m-%d'), False):
                cssclass.append('has-appointment')
            strweek = self._translate(tool.day_msgid(day.weekday()))
            weekdays.append({
                'day': day.day,
                'weekday': strweek[:3],
                'iso': day.isoformat(),
                'cssclass': ' '.join(cssclass),
            })
        return weekdays
