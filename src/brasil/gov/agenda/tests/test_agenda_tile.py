# -*- coding: utf-8 -*-

import unittest

from brasil.gov.agenda.testing import INTEGRATION_TESTING
from brasil.gov.agenda.tiles.agenda import AgendaTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


class AgendaTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u"agenda"
        self.portal.invokeFactory('collective.cover.content', 'frontpage')
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']

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
