# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import PROJECTNAME
from brasil.gov.agenda.interfaces import IBrowserLayer
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers
from zope.site.hooks import setSite

import unittest


class TestBrowserLayer(unittest.TestCase):
    """Ensure browser layer is installed and uninstalled properly."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setSite(portal)
        self.portal = portal
        self.qi = getattr(self.portal, 'portal_quickinstaller')

    def test_installed(self):
        self.assertTrue(IBrowserLayer in registered_layers())

    def test_uninstalled(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertTrue(IBrowserLayer not in registered_layers())
