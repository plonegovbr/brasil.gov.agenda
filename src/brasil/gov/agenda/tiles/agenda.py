# -*- coding: utf-8 -*-
from collective.cover import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from datetime import datetime
from datetime import timedelta
from plone.app.uuid.utils import uuidToObject
from plone.directives import form
# from plone.memoize import forever
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
    form.omitted('monthpicker')
    form.no_omit(IDefaultConfigureForm, 'monthpicker')
    monthpicker = schema.Text(
        title=_(u'Seletor Mês'),
        required=False,
    )
    form.omitted('daypicker')
    form.no_omit(IDefaultConfigureForm, 'daypicker')
    daypicker = schema.Text(
        title=_(u'Seletor Dia'),
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
    index = ViewPageTemplateFile('agenda.pt')
    is_configurable = True
    limit = 1

    def populate_with_object(self, obj):
        super(AgendaTile, self).populate_with_object(obj)  # check permissions

        if obj.portal_type in self.accepted_ct():
            title = _(u'Agenda do {0}').format(obj.autoridade)
            link_url = obj.absolute_url()
            link_text = _(u'Agenda completa')
            uuid = IUUID(obj, None)
            data_mgr = ITileDataManager(self)
            data_mgr.set({
                'title': title,
                'link_url': link_url,
                'link_text': link_text,
                'monthpicker': True,
                'daypicker': True,
                'collection_events': True,
                'agenda_tile_footer': True,
                'agenda_url': obj.absolute_url(),
                'uuid': uuid,
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

    def month(self):
        tool = getToolByName(self.context, 'translation_service')
        today = datetime.now()
        strmonth = self._translate(tool.month_msgid(today.strftime('%m')))
        return {
            'strmonth': strmonth[:3].upper(),
            'month': today.month,
            'year': today.year,
        }

    def days(self):
        agenda = uuidToObject(self.data['uuid'])
        tool = getToolByName(self.context, 'translation_service')
        today = datetime.now()
        # get a list with 3 days before and 3 days after today
        days = [(today + timedelta(i)) for i in xrange(-3, 4)]
        weekdays = []
        for day in days:
            cssclass = ['day']
            if day == today:
                cssclass.append('is-selected')
            if agenda.get(day.strftime('%Y-%m-%d'), False):
                cssclass.append('has-appointment')
            strweek = self._translate(tool.day_msgid(day.weekday()))
            weekdays.append({
                'day': day.day,
                'weekday': strweek[:3],
                'iso': day.isoformat(),
                'cssclass': ' '.join(cssclass),
            })
        return weekdays

    def agenda_diaria(self):
        agenda = uuidToObject(self.data['uuid'])
        agenda_diaria = agenda.get(time.strftime('%Y-%m-%d'), None)
        return agenda_diaria

    @property
    def agenda_url(self):
        return self.data.get('agenda_url', None)

    # @forever.memoize
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
                    'location': compr.location,
                    'description': compr.Title(),
                    'time': compr.start_date.strftime('%Hh%M'),
                }
                collection_events.append(compromisso)
        return collection_events

    def collection_events(self):
        return self._collection_events(self._last_modified())

    # @forever.memoize
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
