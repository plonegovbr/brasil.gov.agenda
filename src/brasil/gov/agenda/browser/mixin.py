# -*- coding: utf-8 -*-
from six.moves import range  # noqa: I001
from brasil.gov.agenda.config import AGENDADIARIAFMT
from datetime import timedelta
from plone import api
from zope.component import getMultiAdapter


class AgendaMixin:
    """Common methods and functions used by views and and tiles."""

    def _translate(self, msgid, locale='plonelocales', mapping=None):
        tool = api.portal.get_tool('translation_service')
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        language = portal_state.language()
        # XXX: Por que é retornado 'pt-br' do portal_state ao invés de 'pt_BR'?
        # Quando uso 'pt-br' ao invés de 'pt_BR', não pega a tradução quando
        # feita de forma manual.
        target_language = 'pt_BR' if language == 'pt-br' else language
        return tool.translate(msgid,
                              locale,
                              mapping=mapping,
                              context=self.context,
                              target_language=target_language)

    def month(self):
        tool = api.portal.get_tool('translation_service')
        strmonth = self._translate(tool.month_msgid(self.date.strftime('%m')))
        return {
            'strmonth': strmonth[:3].upper(),
            'strmonthcomplete': strmonth.upper(),
            'month': self.date.month,
            'year': self.date.year,
        }

    def days(self):
        tool = api.portal.get_tool('translation_service')
        # get a list with 3 days before and 3 days after current day
        days = [(self.date + timedelta(i)) for i in range(-3, 4)]
        weekdays = []
        for day in days:
            cssclass = ['day']
            has_appointment = False
            if day == self.date:
                cssclass.append('is-selected')
            if self.agenda.get(day.strftime(AGENDADIARIAFMT), False):
                has_appointment = True
                cssclass.append('has-appointment')
            # Weekday difference between datetime and DateTime objects
            strweek = self._translate(tool.day_msgid((day.weekday() + 1) % 7))
            weekdays.append({
                'day': day.day,
                'dayurl': day.strftime(AGENDADIARIAFMT),
                'weekday': strweek[:3],
                'cssclass': ' '.join(cssclass),
                'hasappointment': has_appointment,
            })
        return weekdays

    @staticmethod
    def compromissos():
        return []

    @staticmethod
    def exibe_sem_compromissos():
        return True
