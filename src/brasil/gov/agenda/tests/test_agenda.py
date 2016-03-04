# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import AGENDADIARIAFMT
from brasil.gov.agenda.interfaces import IAgenda
from brasil.gov.agenda.testing import FUNCTIONAL_TESTING
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.dexterity.behaviors.nextprevious import INextPreviousToggle
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
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

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('Agenda', 'agenda')
        self.agenda = self.folder['agenda']

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
        agenda.subjects = ('Brasil', 'Governo')
        agenda.reindexObject(idxs=['Subject'])
        ct = self.portal.portal_catalog
        results = ct.searchResults(portal_type='Agenda')
        b = results[0]
        self.assertIn('Brasil', b.Subject)
        self.assertIn('Governo', b.Subject)

    def test_agendadiaria_ordering(self):
        # Create two AgendaDiaria objects
        self.agenda.invokeFactory('AgendaDiaria', '2013-10-17')
        self.agenda.invokeFactory('AgendaDiaria', '2013-02-05')
        oIds = list(self.agenda.objectIds())
        # Sorting should be ascending
        self.assertEqual(['2013-02-05', '2013-10-17'], oIds)
        # Add an older one, should be on top of the list
        self.agenda.invokeFactory('AgendaDiaria', '2012-02-05')
        oIds = list(self.agenda.objectIds())
        self.assertEqual(['2012-02-05', '2013-02-05', '2013-10-17'], oIds)


class ContentTypeBrowserTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.ct = self.portal.portal_catalog
        self.wt = self.portal.portal_workflow

    def setupContent(self, portal):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Criamos a agenda
        self.portal.invokeFactory('Agenda', 'agenda-vice-presidente')
        self.agenda = self.portal['agenda-vice-presidente']
        self.agenda.autoridade = u'Clarice Lispector'
        self.agenda.orgao = u'Presidencia da Republica'
        # Criamos a agenda diaria
        self.agenda.invokeFactory('AgendaDiaria', '2014-02-05')
        self.agendadiaria = self.agenda['2014-02-05']
        self.agendadiaria.date = datetime.datetime(2014, 2, 5)
        self.agendadiaria.reindexObject()
        # Criamos o compromisso
        self.agendadiaria.invokeFactory('Compromisso',
                                        'compromisso',
                                        start_date=datetime.datetime(
                                            2014, 2, 5, 10, 0, 0
                                        ),
                                        end_date=datetime.datetime(
                                            2014, 2, 5, 12, 0, 0
                                        ))
        self.compromisso = self.agendadiaria['compromisso']
        # Publicamos os conteudos
        self.wt.doActionFor(self.agenda, 'publish')
        self.wt.doActionFor(self.agendadiaria, 'publish')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def test_agenda_icon(self):
        app = self.layer['app']
        portal = self.portal

        browser = Browser(app)
        portal_url = portal.absolute_url()

        browser.open('%s/++resource++brasil.gov.agenda/agenda_icon.png' %
                     portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')

    def test_agenda_view(self):
        from plone.app.testing import TEST_USER_NAME
        from plone.app.testing import TEST_USER_PASSWORD
        app = self.layer['app']
        portal = self.portal
        self.setupContent(portal)
        import transaction
        transaction.commit()
        self.browser = Browser(app)
        self.browser.handleErrors = False

        agenda_url = self.agenda.absolute_url()
        browser = self.browser

        # Exibimos uma mensagem de que nao temos
        # compromissos para a data de hoje
        browser.open(agenda_url)
        self.assertIn('existem compromissos agendados.',
                      browser.contents.decode('utf-8'))

        # Criamos uma agenda para o dia de hoje
        hoje = datetime.datetime.now()
        fmt_id = hoje.strftime(AGENDADIARIAFMT)
        fmt_display = hoje.strftime('%d/%m/%Y')
        self.agenda.invokeFactory('AgendaDiaria', fmt_id)
        self.agendahoje = self.agenda[fmt_id]
        self.agendahoje.date = hoje
        self.agendahoje.reindexObject()
        transaction.commit()

        # Como esta AgendaDiaria nao foi publicada, continuamos a
        # exibir a mensagem
        browser.open(agenda_url)
        self.assertIn('existem compromissos agendados.',
                      browser.contents.decode('utf-8'))

        # Ao publicarmos a AgendaDiaria de hoje
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.wt.doActionFor(self.agendahoje, 'publish')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        transaction.commit()
        # Ela se torna a ativa
        browser.open(agenda_url)
        self.assertIn('%s &mdash;' % fmt_display,
                      browser.contents.decode('utf-8'))

        # Nos autenticamos como admin
        browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME,
            TEST_USER_PASSWORD,))
        # Vemos o conteudo da view de Agenda
        browser.open(agenda_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertIn(u'Adicionar Agenda Di',
                      browser.contents.decode('utf-8'))
