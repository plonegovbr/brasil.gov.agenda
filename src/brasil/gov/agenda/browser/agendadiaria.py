# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from brasil.gov.agenda import _
from brasil.gov.agenda.browser.mixin import AgendaMixin
from datetime import datetime
from plone import api
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.i18nmessageid import Message


class AgendaDiariaView(BrowserView, AgendaMixin):
    """Visao padrao da agenda."""

    def setup(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self._ts = api.portal.get_tool('translation_service')
        self.agenda = aq_parent(self.context)
        self.editable = context_state.is_editable()

    def __call__(self):
        self.setup()
        return self.index()

    @property
    def date(self):
        context = self.context
        date = context.date
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
        orgao = self.agenda.orgao
        return orgao

    def autoridade(self):
        autoridade = self.context.autoridade
        if not autoridade:
            autoridade = self.agenda.autoridade
        return autoridade

    def imagem(self):
        imagem = self.agenda.image
        if imagem:
            view = self.agenda.restrictedTraverse('@@images')
            scale = view.scale(fieldname='image', scale='large')
            tag = scale.tag()
            return tag

    def update_info(self):
        update_info = self.context.update
        return getattr(update_info, 'output', '')

    def exibe_sem_compromissos(self):
        compromissos = self.compromissos()
        is_updated = self.update_info()
        # Exibe apenas se nao tivermos compromissos
        # E tambem nao tiver atualizacoes
        return not (compromissos or is_updated)

    def Title(self):
        parts = {}
        parts['weekday'] = self.weekday()
        parts['long_date'] = self.long_date()
        return '%(weekday)s, %(long_date)s' % parts

    def compromissos(self):
        catalog = api.portal.get_tool('portal_catalog')
        now = datetime.now()
        compromissos = []
        query = {}
        query['portal_type'] = 'Compromisso'
        query['sort_on'] = 'start'
        query['path'] = '/'.join(self.context.getPhysicalPath())
        results = catalog.searchResults(**query)
        for brain in results:
            obj = brain.getObject()
            comp = {}
            comp['autoridade'] = self.autoridade()
            comp['title'] = obj.Title()
            comp['solicitante'] = obj.solicitante
            comp['description'] = obj.Description()
            comp['start_time'] = obj.start_date.strftime('%Hh%M')
            comp['start_date'] = obj.start_date.strftime('%Y-%m-%d %H:%M')
            comp['end_time'] = obj.start_date.strftime('%Hh%M')
            comp['end_date'] = obj.end_date.strftime('%Y-%m-%d %H:%M')
            comp['is_now'] = obj.start_date < now < obj.end_date
            comp['location'] = obj.location
            comp['attendees'] = obj.attendees
            # XXX: Preciso formatar esses dados pela view, uma vez que na
            # template causa erros durante o parse do i18ndude.
            # -FATAL- - ERROR in document:
            # <unknown>:55:44: not well-formed (invalid token)
            # No futuro pode ser interessante colocar essa definição no css.
            attendees = ''
            if comp['attendees']:
                attendees = comp['attendees'].split('\n')
            comp['attendees_formatted'] = '<br/>'.join(attendees)
            comp['url'] = obj.absolute_url()
            compromissos.append(comp)
        return compromissos

    def get_link_erros(self):
        portal_obj = self.context.portal_url.getPortalObject()
        if (hasattr(portal_obj, 'relatar-erros')):
            return self.context.absolute_url() + '/relatar-erros'
        else:
            return None
