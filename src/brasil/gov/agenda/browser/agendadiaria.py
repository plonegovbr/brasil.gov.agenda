# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from brasil.gov.agenda.interfaces import IAgendaDiaria
from five import grok
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

grok.templatedir('templates')


class AgendaDiariaView (grok.View):
    """ Visao padrao da agenda
    """

    grok.name('view')
    grok.context(IAgendaDiaria)

    def update(self):
        plone_tools = getMultiAdapter((self.context, self.request),
                                      name='plone_tools')
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self._ts = getToolByName(self.context, 'translation_service')
        self.catalog = plone_tools.catalog()
        self.agenda = aq_parent(self.context)
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
        catalog = self.catalog
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
            comp['description'] = obj.Description()
            comp['start_date'] = obj.start_date
            comp['start_time'] = self._format_time(comp['start_date'])
            comp['start_date'] = obj.start_date.strftime('%Y-%m-%d %H:%M')
            comp['end_date'] = obj.end_date
            comp['end_time'] = self._format_time(comp['end_date'])
            comp['end_date'] = obj.end_date.strftime('%Y-%m-%d %H:%M')
            comp['location'] = obj.location
            comp['attendees'] = obj.attendees
            comp['url'] = obj.absolute_url()
            compromissos.append(comp)
        return compromissos

    def TitleAgenda(self):
        context = self.context
        ctx_parent = context.aq_parent
        title = ctx_parent.Title()
        return title

    def get_link_erros(self):
        portal_obj = self.context.portal_url.getPortalObject()
        if (hasattr(portal_obj, 'relatar-erros')):
            return self.context.absolute_url() + '/relatar-erros'
        else:
            return None
