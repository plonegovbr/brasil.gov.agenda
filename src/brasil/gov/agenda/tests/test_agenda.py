# -*- coding: utf-8 -*-
from brasil.gov.agenda.interfaces import IAgenda
from brasil.gov.agenda.testing import FUNCTIONAL_TESTING
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.dexterity.behaviors.nextprevious import INextPreviousToggle
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing.z2 import Browser
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryUtility

import datetime
import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                container=self.portal, type='Folder', id='test-folder')
        self.agenda = api.content.create(
            container=self.folder, type='Agenda', id='agenda')

    def test_adding(self):
        self.assertTrue(IAgenda.providedBy(self.agenda))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Agenda')
        self.assertIsNotNone(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Agenda')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IAgenda.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.agenda))
        self.assertTrue(IAttributeUUID.providedBy(self.agenda))

    def test_next_previous(self):
        self.assertTrue(INextPreviousToggle.providedBy(self.agenda))

    def test_exclude_from_nav(self):
        self.assertTrue(IExcludeFromNavigation.providedBy(self.agenda))

    def test_exclude_from_nav_default(self):
        behavior = IExcludeFromNavigation(self.agenda)
        self.assertFalse(behavior.exclude_from_nav)

    def test_subjects_catalog(self):
        agenda = self.agenda
        agenda.subjects = (u'Brasil', u'México')
        agenda.reindexObject(idxs=['Subject'])
        ct = self.portal.portal_catalog
        results = ct.searchResults(portal_type='Agenda')
        b = results[0]
        self.assertIn('Brasil', b.Subject)
        self.assertIn('México', b.Subject)

    def test_agendadiaria_ordering(self):
        # Create two AgendaDiaria objects
        api.content.create(container=self.agenda, type='AgendaDiaria', id='2013-10-17')
        api.content.create(container=self.agenda, type='AgendaDiaria', id='2013-02-05')
        oIds = list(self.agenda.objectIds())
        # Sorting should be ascending
        self.assertEqual(['2013-02-05', '2013-10-17'], oIds)
        # Add an older one, should be on top of the list
        api.content.create(container=self.agenda, type='AgendaDiaria', id='2012-02-05')
        oIds = list(self.agenda.objectIds())
        self.assertEqual(['2012-02-05', '2013-02-05', '2013-10-17'], oIds)


class ContentTypeBrowserTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def setupContent(self, portal):
        with api.env.adopt_roles(['Manager']):
            self.agenda = api.content.create(
                container=self.portal,
                type='Agenda',
                id='agenda-vice-presidente',
                autoridade=u'Clarice Lispector',
                orgao=u'Presidencia da Republica',
            )
            # Criamos a agenda diaria
            self.agendadiaria = api.content.create(
                container=self.agenda,
                type='AgendaDiaria',
                id='2014-02-05',
                date=datetime.datetime(2014, 2, 5),
            )
            # Criamos o compromisso
            self.compromisso = api.content.create(
                container=self.agendadiaria,
                type='Compromisso',
                id='compromisso',
                start_date=datetime.datetime(2014, 2, 5, 10, 0, 0),
                end_date=datetime.datetime(2014, 2, 5, 12, 0, 0),
            )
            # Publicamos os conteudos
            api.content.transition(obj=self.agenda, transition='publish')
            api.content.transition(obj=self.agendadiaria, transition='publish')

    def test_agenda_icon(self):
        app = self.layer['app']
        portal = self.portal

        browser = Browser(app)
        portal_url = portal.absolute_url()

        browser.open(
            portal_url + '/++resource++brasil.gov.agenda/img/agenda_icon.png')
        self.assertEqual(browser.headers['status'], '200 Ok')
