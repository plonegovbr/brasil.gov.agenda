# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import PROJECTNAME
from brasil.gov.agenda.testing import FUNCTIONAL_TESTING
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone import api
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
            (u'4003',)
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

    def test_agendadiaria_not_listed(self):
        pp = getattr(self.portal, 'portal_properties')
        navtree_properties = pp.navtree_properties
        metaTypesNotToList = list(navtree_properties.metaTypesNotToList)
        self.assertIn(
            'AgendaDiaria',
            metaTypesNotToList
        )

    def test_compromisso_not_listed(self):
        pp = getattr(self.portal, 'portal_properties')
        navtree_properties = pp.navtree_properties
        metaTypesNotToList = list(navtree_properties.metaTypesNotToList)
        self.assertIn(
            'Compromisso',
            metaTypesNotToList
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

    def test_content_types_added_to_tinymce_linkables(self):
        tinymce = api.portal.get_tool('portal_tinymce')
        self.assertIn('Agenda', tinymce.linkable)
        self.assertIn('AgendaDiaria', tinymce.linkable)
        self.assertIn('Compromisso', tinymce.linkable)


class TestUpgrade(BaseTestCase):
    """Ensure product upgrades work."""

    def setup_content(self):
        # Criamos a agenda
        self.agenda = api.content.create(
            type='Agenda',
            id='agenda',
            container=self.portal
        )
        # Criamos a agenda diaria
        self.agendadiaria = api.content.create(
            type='AgendaDiaria',
            id='2013-02-05',
            container=self.agenda
        )
        self.agendadiaria.date = datetime.datetime(2013, 2, 5)
        self.agendadiaria.update = u'Reuniao em Mirtilo\nVisita Eslovenia'
        self.agendadiaria.autoridade = u'Clarice Lispector'
        self.agendadiaria.location = u'Palacio do Planalto'
        self.agendadiaria.reindexObject()

    def executa_upgrade(self, source, dest):
        # Setamos o profile para versao source
        self.st.setLastVersionForProfile(self.profile, source)
        # Pegamos os upgrade steps
        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        source)
        steps = [step for step in upgradeSteps
                 if (step[0]['dest'] == (dest,))
                 and (step[0]['source'] == (source,))][0]
        # Os executamos
        for step in steps:
            step['step'].doStep(self.st)

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

    def test_to4000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '3000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('4000',))
                and (step[0]['source'] == ('3000',))]
        self.assertEqual(len(step), 1)

    def test_to4001_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '4000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('4001',))
                and (step[0]['source'] == ('4000',))]
        self.assertEqual(len(step), 1)

    def test_to4002_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '4001')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('4002',))
                and (step[0]['source'] == ('4001',))]
        self.assertEqual(len(step), 1)

    def test_2000_fix_agendadiaria(self):
        self.setup_content()
        self.executa_upgrade(u'1000', u'2000')
        self.assertTrue(hasattr(self.agendadiaria.update, 'raw'))
        output = self.agendadiaria.update.output
        self.assertIn('<br', output)
        self.assertIn('Eslovenia', output)
        self.assertIn('Mirtilo', output)

    def test_3000_fix_agendadiaria_catalog(self):
        ct = self.portal.portal_catalog
        self.setup_content()

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

        self.executa_upgrade(u'2000', u'3000')

        results = ct.searchResults(
            path='/'.join(self.agendadiaria.getPhysicalPath())
        )
        self.assertEqual(results[0].Title,
                         u'Agenda de Clarice Lispector para 05/02/2013')

    def test_4000_tile_agenda(self):
        record = 'plone.app.tiles'
        # Remove o tile manualmente
        tiles = list(api.portal.get_registry_record(record))
        if 'agenda' in tiles:
            tiles.remove('agenda')
        api.portal.set_registry_record(record, tiles)
        self.executa_upgrade(u'3000', u'4000')

        tiles = list(api.portal.get_registry_record(record))
        self.assertIn(
            'agenda',
            tiles
        )

    def test_4001_corrige_campo_date(self):
        self.setup_content()
        agendadiaria = self.agendadiaria
        # Campo data sera diferente do id gerado
        agendadiaria.date = datetime.date.today()

        self.executa_upgrade(u'4000', u'4001')

        data = self.agendadiaria.date
        self.assertEqual(
            data.strftime('%Y-%m-%d'),
            self.agendadiaria.getId()
        )

    def test_4002_remove_behavior(self):
        types_tool = self.portal.portal_types
        behavior = 'plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation'

        # Para os testes adicionamos o behavior manualmente
        behaviors = list(types_tool['AgendaDiaria'].behaviors)
        behaviors.append(behavior)
        types_tool['AgendaDiaria'].behaviors = behaviors

        # Para os testes adicionamos o behavior manualmente
        behaviors = list(types_tool['Compromisso'].behaviors)
        behaviors.append(behavior)
        types_tool['Compromisso'].behaviors = behaviors

        self.executa_upgrade(u'4001', u'4002')

        # Removido do tipo AgendaDiaria
        self.assertNotIn(behavior, types_tool['AgendaDiaria'].behaviors)
        # Removido do tipo Compromisso
        self.assertNotIn(behavior, types_tool['Compromisso'].behaviors)

    def test_4002_adiciona_tipos_metaTypesNotToList(self):
        navtree_properties = self.portal.portal_properties.navtree_properties
        metaTypesNotToList = list(navtree_properties.metaTypesNotToList)

        # Para os testes removeremos os tipos manualmente
        types = ['AgendaDiaria', 'Compromisso']
        for pt in types:
            if pt in metaTypesNotToList:
                metaTypesNotToList.remove(pt)

        self.executa_upgrade(u'4001', u'4002')

        # Os tipos devem estar listados novamente
        metaTypesNotToList = list(navtree_properties.metaTypesNotToList)

        # Adicionado o tipo AgendaDiaria
        self.assertIn('AgendaDiaria', metaTypesNotToList)
        # Adicionado o tipo Compromisso
        self.assertIn('Compromisso', metaTypesNotToList)

    def test_4002_aplica_behavior(self):
        types_tool = self.portal.portal_types
        behavior = 'plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation'

        # Para os testes removemos o behavior manualmente
        behaviors = list(types_tool['Agenda'].behaviors)
        behaviors.remove(behavior)
        types_tool['Agenda'].behaviors = behaviors

        self.executa_upgrade(u'4001', u'4002')

        # Removido do tipo AgendaDiaria
        self.assertIn(behavior, types_tool['Agenda'].behaviors)

    def test_4002_atualiza_exclude_from_nav(self):
        ct = self.portal.portal_catalog
        self.setup_content()

        def exclude_from_nav():
            return False

        agendadiaria = self.agendadiaria
        # Monkey patch exclude_from_nav
        setattr(agendadiaria, '_exclude_from_nav', agendadiaria.exclude_from_nav)
        setattr(agendadiaria, 'exclude_from_nav', exclude_from_nav)
        # Reindexa o objeto
        agendadiaria.reindexObject()
        # Testamos que exclude_from_nav agora eh False
        results = ct.searchResults(portal_type='AgendaDiaria')
        b = results[0]
        self.assertFalse(b.exclude_from_nav)

        # Voltamos o comportamento original
        setattr(agendadiaria, 'exclude_from_nav', agendadiaria._exclude_from_nav)

        self.executa_upgrade(u'4001', u'4002')

        results = ct.searchResults(portal_type='AgendaDiaria')
        b = results[0]
        self.assertTrue(b.exclude_from_nav)

    def test_4003_adds_content_types_to_linkables_in_tinymce(self):
        tinymce = api.portal.get_tool('portal_tinymce')

        # simulate TinyMCE state on 4002
        linkable = tinymce.linkable.split()
        linkable.remove('Agenda')
        linkable.remove('AgendaDiaria')
        linkable.remove('Compromisso')
        tinymce.linkable = u'\n'.join(linkable)
        self.assertNotIn('Agenda', tinymce.linkable.split())
        self.assertNotIn('AgendaDiaria', tinymce.linkable.split())
        self.assertNotIn('Compromisso', tinymce.linkable.split())

        self.executa_upgrade(u'4002', u'4003')

        self.assertIn('Agenda', tinymce.linkable.split())
        self.assertIn('AgendaDiaria', tinymce.linkable.split())
        self.assertIn('Compromisso', tinymce.linkable.split())

    def test_4003_updates_indexes(self):
        self.setup_content()
        # modify date field without updating the catalog
        self.agendadiaria.date = datetime.datetime.now()
        catalog = api.portal.get_tool('portal_catalog')
        results = catalog(portal_type='AgendaDiaria')
        assert len(results) == 1
        before = results[0].EffectiveDate

        self.executa_upgrade(u'4002', u'4003')

        results = catalog(portal_type='AgendaDiaria')
        assert len(results) == 1
        after = results[0].EffectiveDate
        self.assertLess(before, after)

    def test_hidden_upgrade_profiles(self):
        upgrades = [
            'brasil.gov.agenda.upgrades.v2000',
            'brasil.gov.agenda.upgrades.v3000',
            'brasil.gov.agenda.upgrades.v4000',
            'brasil.gov.agenda.upgrades.v4001',
            'brasil.gov.agenda.upgrades.v4002',
            'brasil.gov.agenda.upgrades.v4003',
        ]
        packages = [p['id'] for p in self.qi.listInstallableProducts()]
        result = [p for p in upgrades if p in packages]
        self.assertFalse(result,
                         ('Estes upgrades nao estao ocultas: %s' %
                          ', '.join(result)))


class TestUninstall(BaseTestCase):
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
