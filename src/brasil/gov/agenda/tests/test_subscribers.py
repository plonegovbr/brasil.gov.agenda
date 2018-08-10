# -*- coding: utf-8 -*-
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone import api
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import datetime
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


class CompromissoSubscriberTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            folder = api.content.create(
                container=self.portal, type='Folder', id='test-folder')

        date = datetime.datetime(2018, 8, 1)
        self.agenda = api.content.create(
            container=folder, type='Agenda', id='agenda')
        self.day = api.content.create(
            container=self.agenda, type='AgendaDiaria', id='2018-08-01')
        self.day.date = date
        self.appointment = api.content.create(
            container=self.day, type='Compromisso', id='foo', start_date=date)

    def test_create_appointment_on_agenda(self):
        results = api.content.find(portal_type='Compromisso')
        self.assertEqual(len(results), 1)

        # create an appointment on a different date
        date = datetime.datetime(2018, 8, 15)
        # FIXME: creation is raising AttributeError
        #        that could be the cause of issues in production
        try:
            obj = api.content.create(
                container=self.agenda, type='Compromisso', id='bar', start_date=date)
        except AttributeError:
            obj = self.agenda['2018-08-15']['bar']

        # new day was created
        self.assertIn('2018-08-15', self.agenda.objectIds())
        newday = self.agenda['2018-08-15']

        # appointment is there
        self.assertIn('bar', newday.objectIds())

        # check catalog integrity
        results = api.content.find(portal_type='Compromisso')
        self.assertEqual(len(results), 2)
        results = api.content.find(UID=obj.UID())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getPath(), obj.absolute_url_path())
        self.assertEqual(results[0].getObject(), obj)

    def test_create_appointment_on_day(self):
        results = api.content.find(portal_type='Compromisso')
        self.assertEqual(len(results), 1)

        # create another appointment on the same date
        date = datetime.datetime(2018, 8, 1)
        obj = api.content.create(
            container=self.day, type='Compromisso', id='bar', start_date=date)
        self.assertIn('foo', self.day.objectIds())

        # check catalog integrity
        results = api.content.find(portal_type='Compromisso')
        self.assertEqual(len(results), 2)
        results = api.content.find(UID=obj.UID())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getPath(), obj.absolute_url_path())
        self.assertEqual(results[0].getObject(), obj)

    def test_create_appointment_on_different_day(self):
        results = api.content.find(portal_type='Compromisso')
        self.assertEqual(len(results), 1)

        # create another appointment on a different date
        date = datetime.datetime(2018, 8, 15)
        # FIXME: creation is raising AttributeError
        #        that could be the cause of issues in production
        try:
            api.content.create(container=self.day, type='Compromisso', id='bar', start_date=date)
        except AttributeError:
            pass

        # new day was created
        self.assertIn('2018-08-15', self.agenda.objectIds())
        newday = self.agenda['2018-08-15']

        # appointment is not in original day
        self.assertNotIn('bar', self.day.objectIds())
        # but in specified day
        self.assertIn('bar', newday.objectIds())

        # check catalog integrity
        obj = newday['bar']
        results = api.content.find(portal_type='Compromisso')
        self.assertEqual(len(results), 2)
        results = api.content.find(UID=obj.UID())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getPath(), obj.absolute_url_path())
        self.assertEqual(results[0].getObject(), obj)

    def test_edit_appointment(self):
        results = api.content.find(portal_type='Compromisso')
        self.assertEqual(len(results), 1)

        obj = self.appointment
        uid = obj.UID()

        self.assertIn('foo', self.day.objectIds())
        obj.start_date = datetime.datetime(2018, 8, 15)
        notify(ObjectModifiedEvent(obj))
        # new day was created
        self.assertIn('2018-08-15', self.agenda.objectIds())
        newday = self.agenda['2018-08-15']

        # appointment moved from old day
        self.assertNotIn('foo', self.day.objectIds())
        # to new day
        self.assertIn('foo', newday.objectIds())

        # UID not changed
        obj = newday['foo']
        self.assertEqual(uid, obj.UID())

        # check catalog integrity
        results = api.content.find(portal_type='Compromisso')
        self.assertEqual(len(results), 1)
        results = api.content.find(UID=obj.UID())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getPath(), obj.absolute_url_path())
        self.assertEqual(results[0].getObject(), obj)
