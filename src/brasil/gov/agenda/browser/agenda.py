# -*- coding: utf-8 -*-
from brasil.gov.agenda import _
from brasil.gov.agenda.config import AGENDADIARIAFMT
from brasil.gov.agenda.interfaces import ICompromisso
from brasil.gov.agenda.utils import AgendaMixin
from datetime import datetime
from datetime import timedelta
from DateTime import DateTime
from dateutil.tz import tzlocal
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.i18nmessageid import Message
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.publish import mapply

import json


class AgendaView(BrowserView, AgendaMixin):
    """Visao padrao da agenda."""

    def update(self):
        plone_tools = getMultiAdapter((self.context, self.request),
                                      name='plone_tools')
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self._ts = getToolByName(self.context, 'translation_service')
        self.catalog = plone_tools.catalog()
        self.agenda = self.context
        self.workflow = plone_tools.workflow()
        self.editable = context_state.is_editable()

    def __call__(self):
        mapply(self.update, (), self.request)
        # return super(AgendaView, self).__call__()
        agenda_recente = self.agenda_recente()
        if agenda_recente and not self.editable:
            return agenda_recente.restrictedTraverse('@@view')()
        else:
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
            review_state = self.workflow.getInfoFor(agenda, 'review_state')
            agenda = agenda if review_state == 'published' else None
        return agenda

    def _format_time(self, value):
        return value.strftime('%Hh%M')

    def get_link_erros(self):
        portal_obj = self.context.portal_url.getPortalObject()
        if (hasattr(portal_obj, 'relatar-erros')):
            return self.context.absolute_url() + '/relatar-erros'
        else:
            return None

    @property
    def date(self):
        date = DateTime()
        return date

    def weekday(self):
        date = self.date
        return self._translate(self._ts.day_msgid(date.strftime('%w')))

    def long_date(self):
        month = self.month()
        date = self.date
        parts = {}
        parts['day'] = date.strftime('%d')
        parts['month'] = month['strmonthcomplete']
        parts['year'] = date.strftime('%Y')
        return self.context.translate(Message(_(u'long_date_agenda'),
                                              mapping=parts))

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
    """Visao padrao da agenda."""

    def setup(self):
        self._ts = getToolByName(self.context, 'translation_service')

    def publishTraverse(self, request, date):
        """Pega a data da agenda diaria."""
        self.date = date
        return self

    def weekday(self, date):
        return self._translate(self._ts.day_msgid(date.strftime('%w')))

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
                'items': [],
                'hasAppointment': False,
                'isSelected': False,
            }
            if self.date == strday:
                day['isSelected'] = True
            agendadiaria = self.context.get(strday, None)
            if agendadiaria:
                day['hasAppointment'] = True
                compromissos = api.content.find(
                    context=agendadiaria,
                    object_provides=ICompromisso,
                    sort_on='start',
                )
                for brain in compromissos:
                    obj = brain.getObject()
                    day['items'].append({
                        'title': obj.title,
                        'start': obj.start_date.strftime('%Hh%M'),
                        'datetime': '{0}{1}:00'.format(obj.start_date.isoformat(), tzname),
                        'location': obj.location,
                        'href': obj.absolute_url(),
                        'vcal': '{0}/vcal_view'.format(obj.absolute_url()),
                        'isNow': obj.start_date <= now <= obj.end_date,
                    })
            data.append(day)
        return data

    def __call__(self):
        self.setup()
        response = self.request.response
        response.setHeader('content-type', 'application/json')
        return response.setBody(json.dumps(self.extract_data()))
