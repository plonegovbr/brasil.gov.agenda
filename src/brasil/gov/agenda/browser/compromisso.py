# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from brasil.gov.agenda import _
from brasil.gov.agenda.interfaces import ICompromisso
from five import grok
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.i18nmessageid import Message


grok.templatedir('templates')


class CompromissoView (grok.View):
    """ Visao padrao do tipo compromisso
    """
    grok.name('view')
    grok.context(ICompromisso)

    def update(self):
        self._ts = getToolByName(self.context, 'translation_service')
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.current_language = portal_state.language()
        self.agendadiaria = aq_parent(self.context)
        self.agenda = aq_parent(self.agendadiaria)
        self.editable = context_state.is_editable()
        if not self.editable:
            url = self.agendadiaria.absolute_url()
            return self.context.REQUEST.RESPONSE.redirect(url)
        year = self.request.form.get('year', None)
        month = self.request.form.get('month', None)
        if not year or not month:
            url = self.context.absolute_url()
            url += '?month:int={0}&year:int={1}'.format(
                self.date.month,
                self.date.year
            )
            return self.context.REQUEST.RESPONSE.redirect(url)

    def _format_time(self, value):
        return value.strftime('%Hh%M')

    def _translate(self, msgid, locale='plonelocales', mapping=None):
        tool = self._ts
        # XXX: Por que é retornado 'pt-br' do portal_state ao invés de 'pt_BR'?
        # Quando uso 'pt-br' ao invés de 'pt_BR', não pega a tradução quando
        # feita de forma manual.
        target_language = ('pt_BR' if self.current_language == 'pt-br'
                           else self.current_language)
        return tool.translate(msgid,
                              locale,
                              mapping=mapping,
                              context=self.context,
                              target_language=target_language)

    @property
    def date(self):
        context = self.context
        date = context.start_date
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

    def Title(self):
        parts = {}
        parts['weekday'] = self.weekday()
        parts['long_date'] = self.long_date()
        return '%(weekday)s, %(long_date)s' % parts

    def compromisso(self):
        obj = self.context
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
        return comp
