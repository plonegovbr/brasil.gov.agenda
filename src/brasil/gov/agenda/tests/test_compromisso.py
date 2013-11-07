# -*- coding: utf-8 -*-
from brasil.gov.agenda.interfaces import ICompromisso
from brasil.gov.agenda.testing import FUNCTIONAL_TESTING
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from DateTime import DateTime
from plone.app.contenttypes.interfaces import IEvent
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing.z2 import Browser
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import datetime
import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.ct = self.portal.portal_catalog
        self.wt = self.portal.portal_workflow
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Criamos a agenda
        self.portal.invokeFactory('Agenda', 'agenda')
        self.agenda = self.portal['agenda']
        # Criamos a agenda diaria
        self.agenda.invokeFactory('AgendaDiaria', '2013-02-05')
        self.agendadiaria = self.agenda['2013-02-05']
        # Criamos o compromisso
        self.agendadiaria.invokeFactory('Compromisso',
                                        'compromisso',
                                        start_date=datetime.datetime(2013, 2, 5))
        self.compromisso = self.agendadiaria['compromisso']
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def test_adding(self):
        self.assertTrue(ICompromisso.providedBy(self.compromisso))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Compromisso')
        self.assertIsNotNone(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Compromisso')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ICompromisso.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.compromisso))
        self.assertTrue(IAttributeUUID.providedBy(self.compromisso))

    def test_exclude_from_nav(self):
        self.assertTrue(IExcludeFromNavigation.providedBy(self.compromisso))

    def test_ievent(self):
        self.assertTrue(IEvent.providedBy(self.compromisso))

    def test_compromisso_moved_to_new_agenda_diaria(self):
        self.assertIn('compromisso', self.agendadiaria.objectIds())
        self.compromisso.start_date = datetime.datetime(2013, 10, 17)
        notify(ObjectModifiedEvent(self.compromisso))
        # Moved from old AgendaDiaria
        self.assertNotIn('compromisso', self.agendadiaria.objectIds())
        # Moved to new AgendaDiaria
        self.assertIn('compromisso', self.agenda['2013-10-17'].objectIds())

    def test_start_indexing(self):
        ct = self.ct
        results = ct.searchResults(portal_type='Compromisso',
                                   start={'query': DateTime('2013-02-06'),
                                          'range': 'max'})
        self.assertEqual(len(results), 1)
        self.compromisso.start_date = datetime.datetime(2013, 10, 17, 3, 0, 0)
        self.compromisso.reindexObject()
        results = ct.searchResults(portal_type='Compromisso',
                                   start={'query': ('2013-10-17 00:00:00',
                                                    '2013-10-17 08:00:00'),
                                          'range': 'minmax'})
        self.assertEqual(len(results), 1)

    def test_end_indexing(self):
        ct = self.ct
        self.compromisso.end_date = datetime.datetime(2013, 2, 6, 12, 0, 0)
        self.compromisso.reindexObject()
        results = ct.searchResults(portal_type='Compromisso',
                                   end={'query': ('2013-02-06 11:00:00',
                                                  '2013-02-06 16:00:00'),
                                        'range': 'minmax'})
        self.assertEqual(len(results), 1)
        self.compromisso.end_date = datetime.datetime(2013, 10, 17, 4, 0, 0)
        self.compromisso.reindexObject()
        results = ct.searchResults(portal_type='Compromisso',
                                   end={'query': ('2013-10-17 00:00:00',
                                                  '2013-10-17 08:00:00'),
                                        'range': 'minmax'})
        self.assertEqual(len(results), 1)

    def test_location_indexing(self):
        ct = self.ct
        self.compromisso.location = u'Sala 635'
        self.compromisso.reindexObject()
        results = ct.searchResults(portal_type='Compromisso',
                                   location=u'Sala 635')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].location, u'Sala 635')
        self.compromisso.location = u'Palacio do Planalto'
        self.compromisso.reindexObject()
        results = ct.searchResults(portal_type='Compromisso',
                                   location=u'Palacio do Planalto')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].location, u'Palacio do Planalto')


class ContentTypeBrowserTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.ct = self.portal.portal_catalog
        self.wt = self.portal.portal_workflow

    def setupContent(self, portal):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Criamos a agenda
        self.portal.invokeFactory('Agenda', 'agenda-presidente')
        self.agenda = self.portal['agenda-presidente']
        # Criamos a agenda diaria
        self.agenda.invokeFactory('AgendaDiaria', '2014-02-05')
        self.agendadiaria = self.agenda['2014-02-05']
        # Criamos o compromisso
        self.agendadiaria.invokeFactory('Compromisso',
                                        'compromisso',
                                        start_date=datetime.datetime(2014, 2, 5))
        self.compromisso = self.agendadiaria['compromisso']
        # Publicamos os conteudos
        self.wt.doActionFor(self.agenda, 'publish')
        self.wt.doActionFor(self.agendadiaria, 'publish')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def test_compromisso_icon(self):
        app = self.layer['app']
        portal = self.portal

        browser = Browser(app)
        portal_url = portal.absolute_url()

        browser.open('%s/++resource++brasil.gov.agenda/compromisso_icon.png' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')

    def test_compromisso_view(self):
        from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
        app = self.layer['app']
        portal = self.portal
        self.setupContent(portal)
        import transaction
        transaction.commit()
        self.browser = Browser(app)
        self.browser.handleErrors = False

        agendadiaria_url = self.agendadiaria.absolute_url()
        compromisso_url = self.compromisso.absolute_url()
        browser = self.browser

        # Seremos redirecionados se acessarmos a view de compromisso
        # como usuarios anonimos
        browser.open(compromisso_url)
        self.assertEqual(browser.url, agendadiaria_url)

        # Nos autenticamos como admin
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        # Vemos o conteudo
        browser.open(compromisso_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertEqual(browser.url, compromisso_url)

    def test_compromisso_ics(self):
        app = self.layer['app']
        portal = self.portal
        self.setupContent(portal)
        import transaction
        transaction.commit()
        self.browser = Browser(app)
        self.browser.handleErrors = False

        ical_url = '%s/ical_view' % self.compromisso.absolute_url()
        browser = self.browser

        # Acessaremos a view de vcal
        browser.open(ical_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
        # Headers devem indicar dados ICAL
        self.assertIn('text/calendar',
                      browser.headers['content-type'])
        # Corpo deve conter indicacao do produto que o criou
        self.assertIn('BEGIN:VCALENDAR\r\nPRODID:brasil.gov.agenda',
                      browser.contents)
        # E a data de inicio
        self.assertIn('DTSTART:20140205',
                      browser.contents)

    def test_compromisso_vcs(self):
        app = self.layer['app']
        portal = self.portal
        self.setupContent(portal)
        import transaction
        transaction.commit()
        self.browser = Browser(app)
        self.browser.handleErrors = False

        vcal_url = '%s/vcal_view' % self.compromisso.absolute_url()
        browser = self.browser

        # Acessaremos a view de vcal
        browser.open(vcal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
        # Headers devem indicar dados VCAL
        self.assertIn('text/x-vCalendar',
                      browser.headers['content-type'])
        # Corpo deve conter indicacao do produto que o criou
        self.assertIn('BEGIN:VCALENDAR\r\nPRODID:brasil.gov.agenda',
                      browser.contents)
        # E a data de inicio
        self.assertIn('BEGIN:VEVENT\r\nDTSTART:20140205',
                      browser.contents)
