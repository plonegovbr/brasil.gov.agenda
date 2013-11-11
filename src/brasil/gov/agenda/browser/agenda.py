# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import AGENDADIARIAFMT
from brasil.gov.agenda.interfaces import IAgenda
from DateTime import DateTime
from five import grok
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.publisher.publish import mapply

grok.templatedir('templates')


class AgendaView (grok.View):
    """ Visao padrao da agenda
    """

    grok.name('view')
    grok.context(IAgenda)

    def update(self):
        plone_tools = getMultiAdapter((self.context, self.request),
                                      name='plone_tools')
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self._ts = getToolByName(self.context, 'translation_service')
        self.catalog = plone_tools.catalog()
        self.workflow = plone_tools.workflow()
        self.editable = context_state.is_editable()

    def __call__(self):
        mapply(self.update, (), self.request)
        agenda_recente = self.agenda_recente()
        if agenda_recente and not self.editable:
            return agenda_recente.restrictedTraverse('@@view')()
        else:
            return super(AgendaView, self).__call__()

    def _format_time(self, value):
        return value.strftime('%Hh%M')

    def _translate(self, msgid):
        tool = self._ts
        return tool.translate(msgid,
                              'plonelocales',
                              {},
                              context=self.context,
                              target_language='pt_BR')

    def agenda_recente(self):
        """ Retorna a agenda mais publicada mais recente """
        agenda = None
        hoje = DateTime().strftime(AGENDADIARIAFMT)
        # Validamos se existe uma agenda para o dia de hoje
        # e se ela esta publicada
        if hoje in self.context.objectIds():
            agenda = self.context[hoje]
            review_state = self.workflow.getInfoFor(agenda, 'review_state')
            agenda = agenda if review_state == 'published' else None
        if not agenda:
            # Caso nao exista retornamos a agenda mais recente
            ct = self.catalog
            path = '/'.join(self.context.getPhysicalPath())
            params = {}
            params['path'] = path
            params['portal_type'] = 'AgendaDiaria'
            params['review_state'] = 'published'
            params['sort_on'] = 'start'
            params['sort_order'] = 'reverse'
            results = ct.searchResults(**params)
            agenda = results[0].getObject() if results else None
        return agenda

    @property
    def date(self):
        context = self.context
        date = context.date
        return date

    def weekday(self):
        date = self.date
        return self._translate(self._ts.day_msgid(date.strftime('%w')))

    def month(self):
        date = self.date
        return self._translate(self._ts.month_msgid(date.strftime('%m')))

    def long_date(self):
        date = self.date
        parts = {}
        parts['day'] = date.strftime('%d')
        parts['month'] = self.month()
        parts['year'] = date.strftime('%Y')
        return '%(day)s de %(month)s de %(year)s' % parts

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

    def Title(self):
        parts = {}
        parts['weekday'] = self.weekday()
        parts['long_date'] = self.long_date()
        return '%(weekday)s, %(long_date)s' % parts
