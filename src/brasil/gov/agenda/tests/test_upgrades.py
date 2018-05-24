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


class to5000TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'*', u'5000')
        self.request.set('test', True)  # avoid transaction commits on tests

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 4)

    def test_fix_subjects_on_agendas(self):
        # check if the upgrade step is registered
        title = u'Fix None subjects on agendas'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        with api.env.adopt_roles(['Manager']):
            obj = api.content.create(self.portal, 'Agenda', 'foo')

        # simulate issue
        obj.subjects = None

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)
        self.assertEqual(obj.subjects, ())
