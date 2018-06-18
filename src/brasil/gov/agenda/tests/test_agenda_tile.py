# -*- coding: utf-8 -*-

from brasil.gov.agenda.testing import INTEGRATION_TESTING
from brasil.gov.agenda.tiles.agenda import AgendaTile
from collective.cover.tiles.base import IPersistentCoverTile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import datetime
import unittest


class AgendaTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u'agenda'
        # Criamos a capa
        self.portal.invokeFactory('collective.cover.content', 'frontpage')
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']
        # Criamos uma pasta
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        # Criamos uma Agenda
        self.folder.invokeFactory('Agenda', 'agenda')
        self.agenda = self.folder['agenda']
        # Pegamos a data do dia
        now = datetime.datetime.now()
        currentDay = now.day
        currentMonth = now.month
        currentYear = now.year
        currentDate = now.strftime('%Y-%m-%d')
        # Criamos a agenda diaria
        self.agenda.invokeFactory('AgendaDiaria', currentDate)
        self.agendadiaria = self.agenda[currentDate]
        self.agendadiaria.autoridade = u'Clarice Lispector'
        self.agendadiaria.date = datetime.datetime(currentYear, currentMonth, currentDay)
        self.agendadiaria.reindexObject()
        # Criamos o compromisso
        self.agendadiaria.invokeFactory('Compromisso',
                                        'compromisso',
                                        start_date=datetime.datetime(currentYear, currentMonth, currentDay))
        self.compromisso = self.agendadiaria['compromisso']

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(AgendaTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, AgendaTile))
        tile = AgendaTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_tile_is_empty(self):
        # test if tile is empty
        self.assertTrue(self.tile.is_empty())

    def test_collection_events(self):
        # test the return os events in agenda
        # now we add an agenda to the tile
        obj = self.agenda
        self.tile.populate_with_object(obj)
        # tile's data attributed is cached so we should re-instantiate the tile
        tile = getMultiAdapter((self.cover, self.request), name=self.name)
        tile = tile['test']
        # we call collection events for this tile
        collection_events = AgendaTile._collection_events(tile)
        # check if lists the compromisso
        self.assertEqual(
            next(collection_events),
            [{
                'timestamp_class': 'timestamp-cell is-now',
                'time': '00h00',
                'location': u'',
                'description': '',
            }],
        )

    def test_crud(self):
        # we start with an empty tile
        self.assertTrue(self.tile.is_empty())

        # now we add an agenda to the tile
        obj = self.agenda
        self.tile.populate_with_object(obj)

        # tile's data attributed is cached so we should re-instantiate the tile
        tile = getMultiAdapter((self.cover, self.request), name=self.name)
        tile = tile['test']
        self.assertEqual(self.tile.results()['title'], 'Agenda do None')

    def test_accepted_content_types(self):
        # only Agenda is accepted
        self.assertEqual(self.tile.accepted_ct(),
                         ['Agenda'])
