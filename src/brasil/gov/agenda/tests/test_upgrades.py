# -*- coding: utf-8 -*-
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone import api

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.setup = self.portal['portal_setup']
        self.profile_id = u'brasil.gov.agenda:default'
        self.from_version = from_version
        self.to_version = to_version

    def get_upgrade_step(self, title):
        """Get the named upgrade step."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def execute_upgrade_step(self, step):
        """Execute an upgrade step."""
        self.request.form['profile_id'] = self.profile_id
        self.request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=self.request)

    @property
    def total_steps(self):
        """Return the number of steps in the upgrade."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class to4100TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'*', u'4100')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 3)

    def test_fix_resources_references(self):
        title = u'Fix resource references'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        from brasil.gov.agenda.upgrades.v4100 import SWIPER_CSS
        from brasil.gov.agenda.upgrades.v4100 import SWIPER_JS
        from brasil.gov.agenda.upgrades.v4100 import NEW_CSS
        from brasil.gov.agenda.upgrades.v4100 import OLD_CSS
        from brasil.gov.agenda.upgrades.v4100 import NEW_JS

        css_tool = api.portal.get_tool('portal_css')
        css_tool.unregisterResource(SWIPER_CSS)
        css_tool.getResource(NEW_CSS).setCompression('safe')
        css_tool.renameResource(NEW_CSS, OLD_CSS)

        ids = css_tool.getResourceIds()
        self.assertNotIn(SWIPER_CSS, ids)
        self.assertNotIn(NEW_CSS, ids)
        self.assertIn(OLD_CSS, ids)
        self.assertEqual(css_tool.getResource(OLD_CSS).getCompression(), 'safe')

        js_tool = api.portal.get_tool('portal_javascripts')
        js_tool.unregisterResource(SWIPER_JS)
        js_tool.unregisterResource(NEW_JS)

        ids = js_tool.getResourceIds()
        self.assertNotIn(SWIPER_JS, ids)
        self.assertNotIn(NEW_JS, ids)

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)

        ids = css_tool.getResourceIds()
        self.assertEqual(SWIPER_CSS, ids[0])
        self.assertNotIn(OLD_CSS, ids)
        self.assertIn(NEW_CSS, ids)
        self.assertEqual(css_tool.getResource(NEW_CSS).getCompression(), 'none')

        ids = js_tool.getResourceIds()
        self.assertEqual(SWIPER_JS, ids[0])
        self.assertIn(NEW_JS, ids)


class to4101TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'4100', u'4101')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 1)

    def test_import_various(self):
        title = u'Remove portlet registration'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        self.execute_upgrade_step(step)
