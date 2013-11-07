# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import PROJECTNAME
from brasil.gov.agenda.testing import FUNCTIONAL_TESTING
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing.z2 import Browser
from Products.GenericSetup.upgrade import listUpgradeSteps
from zope.site.hooks import setSite

import datetime
import unittest


class Plone43TestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING


class BaseTestCase(unittest.TestCase):
    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    profile = 'brasil.gov.agenda:default'

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUp(self):
        portal = self.layer['portal']
        setSite(portal)
        self.portal = portal
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.wt = getattr(self.portal, 'portal_workflow')
        self.st = getattr(self.portal, 'portal_setup')
        self.setUpUser()


class TestInstall(BaseTestCase):
    """Ensure product is properly installed."""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_version(self):
        self.assertEqual(
            self.st.getLastVersionForProfile(self.profile),
            (u'3000',)
        )

    def test_static_resource_grokker(self):
        """Grok does not register automatically the static resources anymore see:
        http://svn.zope.org/five.grok/trunk/src/five/grok/meta.py?rev=123298&r1=112163&r2=123298
        """
        portal = self.layer['portal']
        app = self.layer['app']

        browser = Browser(app)
        portal_url = portal.absolute_url()

        browser.open('%s/++resource++brasil.gov.agenda' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')

    def test_css_registered(self):
        cssreg = getattr(self.portal, 'portal_css')
        stylesheets_ids = cssreg.getResourceIds()
        self.assertIn(
            '++resource++brasil.gov.agenda/agenda.css',
            stylesheets_ids
        )

    def test_agenda_not_searched(self):
        pp = getattr(self.portal, 'portal_properties')
        site_properties = pp.site_properties
        types_not_searched = site_properties.types_not_searched
        self.assertIn(
            'Agenda',
            types_not_searched
        )

    def test_compromisso_not_searched(self):
        pp = getattr(self.portal, 'portal_properties')
        site_properties = pp.site_properties
        types_not_searched = site_properties.types_not_searched
        self.assertIn(
            'Compromisso',
            types_not_searched
        )

    def test_agendadiaria_in_calendar(self):
        calendar = getattr(self.portal, 'portal_calendar')
        calendar_types = calendar.calendar_types
        self.assertIn(
            'AgendaDiaria',
            calendar_types
        )

    def test_compromisso_not_in_calendar(self):
        calendar = getattr(self.portal, 'portal_calendar')
        calendar_types = calendar.calendar_types
        self.assertNotIn(
            'Compromisso',
            calendar_types
        )

    def test_add_agenda_permission(self):
        permission = 'brasil.gov.agenda: Add Agenda'
        portal = self.portal
        allowed = [x['name']
                   for x in portal.rolesOfPermission(permission)
                   if x['selected']]
        self.assertEqual(allowed,
                         ['Contributor', 'Manager', 'Owner', 'Site Administrator'])

    def test_add_agendadiaria_permission(self):
        permission = 'brasil.gov.agenda: Add AgendaDiaria'
        portal = self.portal
        allowed = [x['name']
                   for x in portal.rolesOfPermission(permission)
                   if x['selected']]
        self.assertEqual(allowed,
                         ['Contributor', 'Manager', 'Owner', 'Site Administrator'])

    def test_add_compromisso_permission(self):
        permission = 'brasil.gov.agenda: Add Compromisso'
        portal = self.portal
        allowed = [x['name']
                   for x in portal.rolesOfPermission(permission)
                   if x['selected']]
        self.assertEqual(allowed,
                         ['Contributor', 'Manager', 'Owner', 'Site Administrator'])


class TestUpgrade(BaseTestCase):
    """Ensure product upgrades work."""

    def test_to2000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '1000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('2000',))
                and (step[0]['source'] == ('1000',))]
        self.assertEqual(len(step), 1)

    def test_to3000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '2000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('3000',))
                and (step[0]['source'] == ('2000',))]
        self.assertEqual(len(step), 1)

    def test_2000_fix_agendadiaria(self):
        # Criamos a agenda
        self.portal.invokeFactory('Agenda', 'agenda')
        self.agenda = self.portal['agenda']
        # Criamos a agenda diaria
        self.agenda.invokeFactory('AgendaDiaria', '2013-02-05')
        self.agendadiaria = self.agenda['2013-02-05']
        self.agendadiaria.date = datetime.datetime(2013, 2, 5)
        self.agendadiaria.update = u'Reuniao em Mirtilo\nVisita Eslovenia'
        self.agendadiaria.reindexObject()
        # Setamos o profile para versao 1000
        self.st.setLastVersionForProfile(self.profile, u'1000')
        # Pegamos os upgrade steps
        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '1000')
        steps = [step for step in upgradeSteps
                 if (step[0]['dest'] == ('2000',))
                 and (step[0]['source'] == ('1000',))][0]
        # Os executamos
        for step in steps:
            step['step'].doStep(self.st)
        self.assertTrue(hasattr(self.agendadiaria.update, 'raw'))
        output = self.agendadiaria.update.output
        self.assertIn('<br', output)
        self.assertIn('Eslovenia', output)
        self.assertIn('Mirtilo', output)

    def test_3000_fix_agendadiaria_catalog(self):
        ct = self.portal.portal_catalog
        # Criamos a agenda
        self.portal.invokeFactory('Agenda', 'agenda')
        self.agenda = self.portal['agenda']
        # Criamos a agenda diaria
        self.agenda.invokeFactory('AgendaDiaria', '2013-02-05')
        self.agendadiaria = self.agenda['2013-02-05']
        self.agendadiaria.date = datetime.datetime(2013, 2, 5)
        self.agendadiaria.autoridade = u'Clarice Lispector'
        self.agendadiaria.location = u'Palacio do Planalto'

        # Fazemos um monkey patch no tipo AgendaDiaria
        def Title():
            return '05/02/2013'

        self.agendadiaria._title = self.agendadiaria.Title
        self.agendadiaria.Title = Title
        self.agendadiaria.reindexObject()
        results = ct.searchResults(
            path='/'.join(self.agendadiaria.getPhysicalPath())
        )
        self.assertEqual(results[0].Title, '05/02/2013')

        # Revertemos o monkey patch
        self.agendadiaria.Title = self.agendadiaria._title

        # Setamos o profile para versao 2000
        self.st.setLastVersionForProfile(self.profile, u'2000')
        # Pegamos os upgrade steps
        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '2000')
        steps = [step for step in upgradeSteps
                 if (step[0]['dest'] == ('3000',))
                 and (step[0]['source'] == ('2000',))][0]
        # Os executamos
        for step in steps:
            step['step'].doStep(self.st)

        results = ct.searchResults(
            path='/'.join(self.agendadiaria.getPhysicalPath())
        )
        self.assertEqual(results[0].Title,
                         u'Agenda de Clarice Lispector para 05/02/2013')


class TestUninstall(BaseTestCase):
    """Ensure product is properly uninstalled."""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))
