# -*- coding: utf-8 -*-
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone import api

import unittest


class AgendaSubscriberTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                container=self.portal, type='Folder', id='test-folder')

    def test_nextprevious_enabled(self):
        from plone.app.dexterity.behaviors.nextprevious import INextPreviousToggle
        agenda = api.content.create(
            container=self.folder, type='Agenda', id='agenda')
        self.assertTrue(INextPreviousToggle.providedBy(agenda))
        self.assertTrue(agenda.nextPreviousEnabled)
