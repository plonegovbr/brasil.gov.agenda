# -*- coding: utf-8 -*-
from brasil.gov.agenda import _
from brasil.gov.agenda.interfaces import IAgendaDiaria
from brasil.gov.agenda.utils import AgendaMixin
from DateTime import DateTime
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.i18nmessageid import Message
from zope.publisher.publish import mapply


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
        brains = api.content.find(
            context=self.context,
            object_provides=IAgendaDiaria,
            sort_on='id',
            sort_order='reverse',
            sort_limit=1,
            review_state='published',
        )
        if not brains:
            return None
        return brains[0].getObject()

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
