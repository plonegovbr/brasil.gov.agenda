# -*- coding: utf-8 -*-

from collective.cover import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.directives import form
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema

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
    period = schema.TextLine(
        title=_(u'Period'),
        required=False,
    )
    form.omitted('lastest_update')
    form.no_omit(IDefaultConfigureForm, 'lastest_update')
    lastest_update = schema.TextLine(
        title=_(u'Lastest update'),
        required=False,
    )
    form.omitted('collection_events')
    form.no_omit(IDefaultConfigureForm, 'collection_events')
    collection_events = schema.TextLine(
        title=_(u'Collection events'),
        required=False,
    )
    form.omitted('agenda_tile_footer')
    form.no_omit(IDefaultConfigureForm, 'agenda_tile_footer')
    agenda_tile_footer = schema.TextLine(
        title=_(u'Agenda tile footer'),
        required=False,
    )

    form.no_omit('link_text')
    form.omitted(IDefaultConfigureForm, 'link_text')
    link_text = schema.TextLine(
        title=_(u'Link text'),
        required=False,
    )
    form.no_omit('link_url')
    form.omitted(IDefaultConfigureForm, 'link_url')
    link_url = schema.TextLine(
        title=_(u'Link url'),
        required=False,
    )


class AgendaTile(PersistentCoverTile):
    index = ViewPageTemplateFile("templates/agenda.pt")
    is_configurable = True
    limit = 1

    def populate_with_object(self, obj):
        super(AgendaTile, self).populate_with_object(obj)  # check permissions

        if obj.portal_type in self.accepted_ct():
            title = _(u'Agenda do {0}').format(obj.autoridade)
            path = '/'.join(obj.getPhysicalPath())
            link_url = obj.absolute_url()
            link_text = _(u'Acesse a agenda do {0}').format(obj.autoridade)
            uuid = IUUID(obj)
            data_mgr = ITileDataManager(self)
            data_mgr.set({
                'title': title,
                'path': path,
                'link_url': link_url,
                'link_text': link_text,
                'period': True,
                'lastest_update': True,
                'collection_events': True,
                'agenda_tile_footer': True,
                'uuid': uuid
            })

    def period(self):
        return u'01 de Dezembro de 2013'

    def lastest_update(self):
        return u'Última atualização: 13h55'

    def collection_events(self):
        return [
            {
                'time': '11h56',
                'description': 'Lorem ipsum dolor sitam etcon setetur adipiscing volupt',
            },
            {
                'time': '11h56',
                'description': 'Lorem ipsum dolor sitam etcon setetur adipiscing volupt',
            },
            {
                'time': '11h56',
                'description': 'Lorem ipsum dolor sitam etcon setetur adipiscing volupt',
            },
            {
                'time': '11h56',
                'description': 'Lorem ipsum dolor sitam etcon setetur adipiscing volupt',
            },
            {
                'time': '11h56',
                'description': 'Lorem ipsum dolor sitam etcon setetur adipiscing volupt',
            },
            {
                'time': '11h56',
                'description': 'Lorem ipsum dolor sitam etcon setetur adipiscing volupt',
            },
        ]

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['Agenda']
