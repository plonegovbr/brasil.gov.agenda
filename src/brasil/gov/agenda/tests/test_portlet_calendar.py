# -*- coding: utf-8 -*-

from brasil.gov.agenda.interfaces import IBrowserLayer
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from collective.portlet.calendar import calendar
from collective.portlet.calendar.browser.interfaces import ICalendarExLayer
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import datetime
import unittest


class CalendarPortletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.browser = Browser(self.layer['app'])
        # Marca o request
        noLongerProvides(self.request, ICalendarExLayer)
        alsoProvides(self.request, IBrowserLayer)
        alsoProvides(self.request, ICalendarExLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.folder = api.content.create(
            type='Folder',
            id='test-folder',
            container=self.portal,
        )
        self.agenda = api.content.create(
            type='Agenda',
            id='agenda',
            container=self.folder,
        )
        self.agendadiaria = api.content.create(
            type='AgendaDiaria',
            id='2014-03-29',
            container=self.agenda,
        )
        self.agendadiaria.date = datetime.date(2014, 3, 29)
        self.agendadiaria.reindexObject()

    def test_renderer(self):
        context = self.agenda
        request = self.agenda.REQUEST
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.agenda)
        assignment = calendar.Assignment(root='/test-folder/agenda')

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        renderer.year = '2014'
        renderer.month = '03'
        self.assertTrue(isinstance(renderer, calendar.Renderer))
        self.assertTrue(renderer.is_agenda())
        self.assertEqual(renderer.root_url(), 'http://nohost/plone/test-folder/agenda')
        self.assertEqual(len(renderer.get_agendasdiarias()), 1)

    def test_custom_js_portlet_calendar(self):
        applyProfile(self.portal, 'plone.app.contenttypes:default')
        resource_url = '{0}/{1}'.format(
            self.portal.absolute_url(),
            '++resource++plone.app.event.portlet_calendar.js',
        )
        # Customizamos o js em
        # https://github.com/plone/plone.app.event/blob/1.1.8/plone/app/event/portlets/portlet_calendar.js
        # justamente para remover o 'tooltip': portanto, fazemos um teste
        # simples verificando que ele foi removido.
        removed_word = 'tooltip'
        self.browser.open(resource_url)
        contents = self.browser.contents
        self.assertNotIn(removed_word, contents)
