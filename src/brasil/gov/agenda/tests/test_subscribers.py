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


class AgendaDiariaSubscriberTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            folder = api.content.create(
                container=self.portal, type='Folder', id='test-folder')

        self.agenda = api.content.create(
            container=folder, type='Agenda', id='agenda')

    def test_sort_order(self):
        # create content in opposite order
        for day in ('03', '02', '01'):
            id_ = '2018-08-' + day
            api.content.create(
                container=self.agenda, type='AgendaDiaria', id=id_)

        # check is ordered by id
        expected = ['2018-08-01', '2018-08-02', '2018-08-03']
        self.assertEqual(self.agenda.objectIds(), expected)
