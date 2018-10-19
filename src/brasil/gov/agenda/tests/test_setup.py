# -*- coding: utf-8 -*-
from brasil.gov.agenda.config import PROJECTNAME
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.site.hooks import setSite

import unittest


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


class InstallTestCase(BaseTestCase):
    """Ensure product is properly installed."""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_version(self):
        self.assertEqual(
            self.st.getLastVersionForProfile(self.profile), (u'4104',))

    def test_agenda_not_searched(self):
        pp = getattr(self.portal, 'portal_properties')
        site_properties = pp.site_properties
        types_not_searched = site_properties.types_not_searched
        self.assertIn('Agenda', types_not_searched)

    def test_compromisso_not_searched(self):
        pp = getattr(self.portal, 'portal_properties')
        site_properties = pp.site_properties
        types_not_searched = site_properties.types_not_searched
        self.assertIn('Compromisso', types_not_searched)

    def test_agendadiaria_not_listed(self):
        pp = getattr(self.portal, 'portal_properties')
        navtree_properties = pp.navtree_properties
        metaTypesNotToList = list(navtree_properties.metaTypesNotToList)
        self.assertIn('AgendaDiaria', metaTypesNotToList)

    def test_compromisso_not_listed(self):
        pp = getattr(self.portal, 'portal_properties')
        navtree_properties = pp.navtree_properties
        metaTypesNotToList = list(navtree_properties.metaTypesNotToList)
        self.assertIn('Compromisso', metaTypesNotToList)

    def test_agendadiaria_in_calendar(self):
        calendar = getattr(self.portal, 'portal_calendar')
        calendar_types = calendar.calendar_types
        self.assertIn('AgendaDiaria', calendar_types)

    def test_compromisso_not_in_calendar(self):
        calendar = getattr(self.portal, 'portal_calendar')
        calendar_types = calendar.calendar_types
        self.assertNotIn('Compromisso', calendar_types)

    def test_add_agenda_permission(self):
        permission = 'brasil.gov.agenda: Add Agenda'
        portal = self.portal
        allowed = [x['name']
                   for x in portal.rolesOfPermission(permission)
                   if x['selected']]
        self.assertEqual(
            allowed,
            ['Contributor', 'Manager', 'Owner', 'Site Administrator'])

    def test_add_agendadiaria_permission(self):
        permission = 'brasil.gov.agenda: Add AgendaDiaria'
        portal = self.portal
        allowed = [x['name']
                   for x in portal.rolesOfPermission(permission)
                   if x['selected']]
        self.assertEqual(
            allowed,
            ['Contributor', 'Manager', 'Owner', 'Site Administrator'])

    def test_add_compromisso_permission(self):
        permission = 'brasil.gov.agenda: Add Compromisso'
        portal = self.portal
        allowed = [x['name']
                   for x in portal.rolesOfPermission(permission)
                   if x['selected']]
        self.assertEqual(
            allowed,
            ['Contributor', 'Manager', 'Owner', 'Site Administrator'])

    def test_content_types_added_to_tinymce_linkables(self):
        tinymce = api.portal.get_tool('portal_tinymce')
        self.assertIn('Agenda', tinymce.linkable)
        self.assertIn('AgendaDiaria', tinymce.linkable)
        self.assertIn('Compromisso', tinymce.linkable)


class UninstallTestCase(BaseTestCase):
    """Ensure product is properly uninstalled."""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_content_types_removed_from_tinymce_linkables(self):
        tinymce = api.portal.get_tool('portal_tinymce')
        self.assertNotIn('Agenda', tinymce.linkable)
        self.assertNotIn('AgendaDiaria', tinymce.linkable)
        self.assertNotIn('Compromisso', tinymce.linkable)
