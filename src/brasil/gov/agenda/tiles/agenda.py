# -*- coding: utf-8 -*-

from collective.cover import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.app.uuid.utils import uuidToObject
from plone.directives import form
from plone.memoize import forever
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getMultiAdapter

import time


class IAgendaTile(IPersistentCoverTile):
    """
    """

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )
    form.omitted('period')
    form.no_omit(IDefaultConfigureForm, 'period')
    period = schema.Text(
        title=_(u'Data'),
        required=False,
    )
    form.omitted('lastest_update')
    form.no_omit(IDefaultConfigureForm, 'lastest_update')
    lastest_update = schema.Text(
        title=_(u'Última atualização'),
        required=False,
    )
    form.omitted('collection_events')
    form.no_omit(IDefaultConfigureForm, 'collection_events')
    collection_events = schema.Text(
        title=_(u'Compromissos'),
        required=False,
    )
    form.omitted('agenda_tile_footer')
    form.no_omit(IDefaultConfigureForm, 'agenda_tile_footer')
    agenda_tile_footer = schema.Text(
        title=_(u'Rodapé da Agenda'),
        required=False,
    )

    form.no_omit('link_text')
    form.omitted(IDefaultConfigureForm, 'link_text')
    link_text = schema.TextLine(
        title=_(u'Texto do rodapé'),
        required=False,
    )
    form.no_omit('link_url')
    form.omitted(IDefaultConfigureForm, 'link_url')
    link_url = schema.TextLine(
        title=_(u'Link do rodapé'),
        required=False,
    )


class AgendaTile(PersistentCoverTile):
    index = ViewPageTemplateFile('templates/agenda.pt')
    is_configurable = True
    limit = 1

    def populate_with_object(self, obj):
        super(AgendaTile, self).populate_with_object(obj)  # check permissions

        if obj.portal_type in self.accepted_ct():
            title = _(u'Agenda do {0}').format(obj.autoridade)
            link_url = obj.absolute_url()
            link_text = _(u'Acesse a agenda do {0}').format(obj.autoridade)
            uuid = IUUID(obj, None)
            data_mgr = ITileDataManager(self)
            data_mgr.set({
                'title': title,
                'link_url': link_url,
                'link_text': link_text,
                'period': True,
                'lastest_update': True,
                'collection_events': True,
                'agenda_tile_footer': True,
                'uuid': uuid
            })

    def _last_modified(self):
        agenda = uuidToObject(self.data['uuid'])
        last_modified = int(agenda.modified().strftime('%s'))
        agenda_diaria = agenda.get(time.strftime('%Y-%m-%d'), None)
        if agenda_diaria:
            modified = int(agenda_diaria.modified().strftime('%s'))
            if modified > last_modified:
                last_modified = modified
            for compromisso in agenda_diaria.objectValues():
                modified = int(compromisso.modified().strftime('%s'))
                if modified > last_modified:
                    last_modified = modified
        return last_modified

    def _translate(self, msgid):
        tool = getToolByName(self.context, 'translation_service')
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        current_language = portal_state.language()
        # XXX: Por que é retornado 'pt-br' do portal_state ao invés de 'pt_BR'?
        # Quando uso 'pt-br' ao invés de 'pt_BR', não pega a tradução quando
        # feita de forma manual.
        target_language = ('pt_BR' if current_language == 'pt-br'
                           else current_language)
        return tool.translate(msgid,
                              'plonelocales',
                              {},
                              context=self.context,
                              target_language=target_language)

    def _month(self):
        tool = getToolByName(self.context, 'translation_service')
        return self._translate(tool.month_msgid(time.strftime('%m')))

    @forever.memoize
    def _period(self, last_modified=None):
        parts = {}
        parts['day'] = time.strftime('%d')
        parts['month'] = self._month().lower()
        parts['year'] = time.strftime('%Y')
        return '%(day)s de %(month)s de %(year)s' % parts

    def period(self):
        return self._period(self._last_modified())

    @forever.memoize
    def _lastest_update(self, last_modified=None):
        agenda = uuidToObject(self.data['uuid'])
        agenda_diaria = agenda.get(time.strftime('%Y-%m-%d'), None)
        if agenda_diaria:
            update_info = agenda_diaria.update
            return getattr(update_info, 'output', '')

    def lastest_update(self):
        return self._lastest_update(self._last_modified())

    def agenda_diaria(self):
        agenda = uuidToObject(self.data['uuid'])
        agenda_diaria = agenda.get(time.strftime('%Y-%m-%d'), None)
        return agenda_diaria

    @forever.memoize
    def _collection_events(self, last_modified=None):
        agenda_diaria = self.agenda_diaria()
        collection_events = []
        if agenda_diaria:
            catalog = getToolByName(self.context, 'portal_catalog')
            query = {}
            query['portal_type'] = 'Compromisso'
            query['sort_on'] = 'start'
            query['path'] = '/'.join(agenda_diaria.getPhysicalPath())
            results = catalog.searchResults(**query)
            for brain in results:
                compr = brain.getObject()
                compromisso = {
                    'time': compr.start_date.strftime('%Hh%M'),
                    'description': compr.Title()
                }
                collection_events.append(compromisso)
        return collection_events

    def collection_events(self):
        return self._collection_events(self._last_modified())

    @forever.memoize
    def _url_agenda(self, last_modified=None):
        agenda = uuidToObject(self.data['uuid'])
        agenda_diaria = agenda.get(time.strftime('%Y-%m-%d'), None)
        if agenda_diaria:
            return agenda_diaria.absolute_url()

    def url_agenda(self):
        return self._url_agenda(self._last_modified())

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['Agenda']

    def results(self):
        """ Return the list of objects stored in the tile.
        """
        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        return data

    def is_empty(self):
        data = self.results()
        return data['title'] is None
