# -*- coding: utf-8 -*-
from brasil.gov.agenda.behaviors.date import NameFromDate
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import datetime
import unittest


class NameFromDateTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_behavior_agendadiaria_without_date(self):
        fti = queryUtility(IDexterityFTI, name='AgendaDiaria')
        factory = fti.factory
        new_object = createObject(factory)
        new_object.date = None
        behavior = NameFromDate(new_object)
        self.assertIsNone(behavior)

    def test_behavior_agendadiaria_with_date(self):
        fti = queryUtility(IDexterityFTI, name='AgendaDiaria')
        factory = fti.factory
        new_object = createObject(factory)
        new_object.date = datetime.date(2012, 3, 29)
        behavior = NameFromDate(new_object)
        self.assertEqual(behavior.title, '2012-03-29')
