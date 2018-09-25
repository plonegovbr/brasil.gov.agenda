# -*- coding: utf-8 -*-
from six.moves import range  # noqa: I001
from brasil.gov.agenda.browser.mixin import AgendaMixin
from brasil.gov.agenda.config import AGENDADIARIAFMT
from brasil.gov.agenda.interfaces import IAgendaDiaria
from brasil.gov.agenda.interfaces import ICompromisso
from calendar import monthrange
from datetime import datetime
from datetime import timedelta
from DateTime import DateTime
from dateutil.tz import tzlocal
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.batching import Batch
from Products.Five.browser import BrowserView
from zExceptions import NotFound
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


class AgendaView(BrowserView, AgendaMixin):
    """Visao padrao da agenda."""

    def setup(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self._ts = api.portal.get_tool('translation_service')
        self.agenda = self.context
        self.editable = context_state.is_editable()
        self.date = datetime.now()

    def results(self, b_size=16):
        """Retorna as ultimas agendas diárias"""
        query = {
            'context': self.context,
            'object_provides': IAgendaDiaria,
            'sort_on': 'Date',
            'sort_order': 'reverse',
        }
        b_start = int(self.request.get('b_start', 0))
        results = api.content.find(**query)
        results = IContentListing(results)
        results = Batch(results, b_size, b_start)
        return results

    def __call__(self):
        self.setup()
        agenda_recente = self.agenda_recente()
        if agenda_recente and not self.editable:
            response = self.request.response
            response.redirect(agenda_recente.absolute_url())
        return super(AgendaView, self).__call__()

    def agenda_recente(self):
        """Deve retornar a agendadiaria para o dia atual
           caso contrario exibimos
        """
        agenda = None
        hoje = DateTime().strftime(AGENDADIARIAFMT)
        # Validamos se existe uma agenda para o dia de hoje
        # e se ela esta publicada
        if hoje in self.context.objectIds():
            agenda = self.context[hoje]
            review_state = api.content.get_state(agenda)
            if review_state == 'published':
                return agenda

    def get_link_erros(self):
        portal_obj = self.context.portal_url.getPortalObject()
        if (hasattr(portal_obj, 'relatar-erros')):
            return self.context.absolute_url() + '/relatar-erros'
        else:
            return None

    def orgao(self):
        orgao = self.context.orgao
        return orgao

    def autoridade(self):
        autoridade = self.context.autoridade
        return autoridade

    def imagem(self):
        imagem = self.context.image
        if imagem:
            view = self.context.restrictedTraverse('@@images')
            scale = view.scale(fieldname='image', scale='large')
            tag = scale.tag()
            return tag


@implementer(IPublishTraverse)
class AgendaJSONView(BrowserView, AgendaMixin):
    """JSON view."""

    def publishTraverse(self, request, date):
        """Get the selected date."""
        try:
            datetime.strptime(date, AGENDADIARIAFMT)
        except ValueError:  # invalid date format
            raise NotFound

        self.date = date
        return self

    def weekday(self, date):
        ts = api.portal.get_tool('translation_service')
        return self._translate(ts.day_msgid(date.strftime('%w')))

    def days_with_appointments(self, date):
        first_day = datetime(date.year, date.month, 1)
        _, last_day = monthrange(date.year, date.month)
        last_day = datetime(date.year, date.month, last_day)

        previous_month = first_day - timedelta(days=1)
        next_month = last_day + timedelta(days=1)

        previous_month_first_day = DateTime(
            previous_month.year, previous_month.month, 1)
        _, next_month_last_day = monthrange(next_month.year, next_month.month)
        next_month_last_day = DateTime(
            next_month.year, next_month.month, next_month_last_day)

        date_range_query = {
            'query': (previous_month_first_day, next_month_last_day), 'range': 'min:max'}
        appointments = api.content.find(
            context=self.context,
            object_provides=ICompromisso,
            sort_on='start',
            start=date_range_query,
        )
        # get days with appointments (unique)
        appointments = set(b.start.strftime(AGENDADIARIAFMT) for b in appointments)
        # transform back to list
        return [day for day in appointments]

    def extract_data(self):
        data = []
        now = datetime.now()
        tzname = datetime.now(tzlocal()).tzname()
        selected = datetime.strptime(self.date, AGENDADIARIAFMT)
        days = [selected + timedelta(days=i) for i in range(-3, 4)]
        for date in days:
            strday = date.strftime(AGENDADIARIAFMT)
            day = {
                'datetime': '{0}{1}:00'.format(date.isoformat(), tzname),
                'day': date.day,
                'weekday': self.weekday(date)[:3],
                'update': '',
                'hasAppointment': False,
                'isSelected': False,
            }
            data.append(day)
            appointments = []
            agendadiaria = self.context.get(strday, None)
            if agendadiaria:
                update_info = agendadiaria.update
                day['update'] = getattr(update_info, 'output', '')
                # FIXME: this is slow, use listFolderContents instead
                appointments = api.content.find(
                    context=agendadiaria,
                    object_provides=ICompromisso,
                    sort_on='start',
                )
            if appointments:
                day['hasAppointment'] = True
            if self.date != strday:
                continue
            day['isSelected'] = True
            # just need items into current day
            day['items'] = []
            for brain in appointments:
                obj = brain.getObject()
                day['items'].append({
                    'title': obj.title,
                    'start': obj.start_date.strftime('%Hh%M'),
                    'datetime': '{0}{1}:00'.format(obj.start_date.isoformat(), tzname),
                    'location': obj.location,
                    'href': obj.absolute_url(),
                    'isNow': obj.start_date <= now <= obj.end_date,
                })
            day['daysWithAppointments'] = self.days_with_appointments(date)
        return data

    def __call__(self):
        response = self.request.response
        response.setHeader('content-type', 'application/json')
        return response.setBody(json.dumps(self.extract_data()))
