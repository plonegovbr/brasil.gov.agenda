# -*- coding: utf-8 -*-
from six.moves import range  # noqa: I001
from datetime import datetime
from datetime import timedelta
from plone import api
from zope.component import getMultiAdapter


class AgendaMixin:
    """Common methods and functions used by views and and tiles."""

    def _translate(self, msgid, locale='plonelocales', mapping=None):
        tool = api.portal.get_tool('translation_service')
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
        tool = api.portal.get_tool('translation_service')
        today = datetime.now()
        strmonth = self._translate(tool.month_msgid(today.strftime('%m')))
        return {
            'strmonth': strmonth[:3].upper(),
            'strmonthcomplete': strmonth.upper(),
            'month': today.month,
            'year': today.year,
        }

    def days(self):
        tool = api.portal.get_tool('translation_service')
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

    @staticmethod
    def compromissos():
        return []

    @staticmethod
    def exibe_sem_compromissos():
        return True
