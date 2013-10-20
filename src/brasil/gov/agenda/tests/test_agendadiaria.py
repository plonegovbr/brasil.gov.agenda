# -*- coding: utf-8 -*-

from brasil.gov.agenda.interfaces import IAgendaDiaria
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryUtility

import unittest2 as unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        # Criamos a agenda
        self.folder.invokeFactory('Agenda', 'agenda')
        self.agenda = self.folder['agenda']
        # Criamos a agenda diaria
        self.agenda.invokeFactory('AgendaDiaria', '2013-02-05')
        self.agendadiaria = self.agenda['2013-02-05']

    def test_adding(self):
        self.assertTrue(IAgendaDiaria.providedBy(self.agendadiaria))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='AgendaDiaria')
        self.assertIsNotNone(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='AgendaDiaria')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IAgendaDiaria.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.agendadiaria))
        self.assertTrue(IAttributeUUID.providedBy(self.agendadiaria))

    def test_exclude_from_nav(self):
        self.assertTrue(IExcludeFromNavigation.providedBy(self.agendadiaria))

    def test_agendadiaria_icon(self):
        from plone.testing.z2 import Browser
        portal = self.portal
        app = self.layer['app']

        browser = Browser(app)
        portal_url = portal.absolute_url()

        browser.open('%s/++resource++brasil.gov.agenda/agenda_icon.png' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
