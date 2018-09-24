# -*- coding: utf-8 -*-
from brasil.gov.agenda.browser.mixin import AgendaMixin
from collective.cover import _
from collective.cover.browser.scaling import ImageScale
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from datetime import datetime
from plone import api
from plone.app.imaging.utils import getAllowedSizes
from plone.app.uuid.utils import uuidToObject
from plone.autoform import directives as form
from plone.namedfile import field
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema

import time


class IAgendaTile(IPersistentCoverTile):
    """
    """

    image = field.NamedBlobImage(
        title=_(u'Image'),
        required=False,
    )

    image_description = schema.TextLine(
        title=_(u'Image description'),
        required=False,
        default=u'',
    )

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


class AgendaTile(PersistentCoverTile, AgendaMixin):
    index = ViewPageTemplateFile('agenda.pt')
    is_configurable = True
    limit = 1
    page_size = 3  # items by swiper slide

    def __init__(self, context, request):
        super(AgendaTile, self).__init__(context, request)
        self.setup()

    def setup(self):
        self.date = datetime.now()

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
                'uuid': uuid,
            })

    def _last_modified(self):
        last_modified = int(self.agenda.modified().strftime('%s'))
        agenda_diaria = self.agenda.get(time.strftime('%Y-%m-%d'), None)
        if agenda_diaria:
            modified = int(agenda_diaria.modified().strftime('%s'))
            if modified > last_modified:
                last_modified = modified
            for compromisso in agenda_diaria.objectValues():
                modified = int(compromisso.modified().strftime('%s'))
                if modified > last_modified:
                    last_modified = modified
        return last_modified

    @property
    def agenda(self):
        return uuidToObject(self.data['uuid'])

    def agenda_diaria(self):
        return self.agenda.get(time.strftime('%Y-%m-%d'), None)

    @property
    def agenda_url(self):
        return self.agenda.absolute_url()

    def _collection_events(self, last_modified=None):
        agenda_diaria = self.agenda_diaria()
        page = []
        if agenda_diaria:
            now = datetime.now()
            catalog = api.portal.get_tool('portal_catalog')
            query = {}
            query['portal_type'] = 'Compromisso'
            query['sort_on'] = 'start'
            query['path'] = '/'.join(agenda_diaria.getPhysicalPath())
            results = catalog.searchResults(**query)
            for i, brain in enumerate(results):
                compr = brain.getObject()
                timestamp_class = ['timestamp-cell']
                if compr.start_date < now < compr.end_date:
                    timestamp_class.append('is-now')
                compromisso = {
                    'location': compr.location,
                    'description': compr.Title(),
                    'time': compr.start_date.strftime('%Hh%M'),
                    'timestamp_class': ' '.join(timestamp_class),
                }
                page.append(compromisso)
                is_third_item = (i + 1) % self.page_size == 0
                if is_third_item:
                    yield page
                    page = []
            if page:
                yield page

    def collection_events(self):
        return self._collection_events(self._last_modified())

    def _url_agenda(self, last_modified=None):
        agenda_diaria = self.agenda.get(time.strftime('%Y-%m-%d'), None)
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

    def get_srcset(self):
        data = self.data.get('image')
        scale_view = ImageScale(self, self.request, data=data, fieldname='')
        base_url, ext = scale_view.url.rsplit('.', 1)
        sizes = [(s, w, h) for s, (w, h) in getAllowedSizes().iteritems()]
        srcset = ''
        for i, (scale, width, height) in enumerate(sorted(sizes, key=lambda x: x[1])):
            srcset += '{0}image/{1} {2}w'.format(base_url, scale, width)
            if i + 1 < len(sizes):
                srcset += ', '
        return srcset
