# -*- coding: utf-8 -*-

from brasil.gov.agenda.interfaces import IAgenda
from five import grok
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

grok.templatedir('templates')


class AgendaView (grok.View):
    ''' Visao padrao da agenda
    '''

    grok.name('view')
    grok.context(IAgenda)

    def update(self):
        plone_tools = getMultiAdapter((self.context, self.request),
                                      name='plone_tools')
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self._ts = getToolByName(self.context, 'translation_service')
        self.catalog = plone_tools.catalog()
        self.editable = context_state.is_editable()

    def _format_time(self, value):
        return value.strftime('%Hh%M')

    def _translate(self, msgid):
        tool = self._ts
        return tool.translate(msgid,
                              'plonelocales',
                              {},
                              context=self.context,
                              target_language='pt_BR')

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
