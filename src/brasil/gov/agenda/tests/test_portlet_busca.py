# -*- coding: utf-8 -*-

from brasil.gov.agenda.portlets import busca
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from Products.GenericSetup.utils import _getDottedName
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class BuscaPortletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('Agenda', 'agenda')
        self.agenda = self.folder['agenda']

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name='brasil.gov.agenda.busca')
        self.assertEqual(portlet.addview, 'brasil.gov.agenda.busca')

    def test_registered_interfaces(self):
        portlet = getUtility(IPortletType, name='brasil.gov.agenda.busca')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEqual(
            ['plone.app.portlets.interfaces.IColumn',
             'plone.app.portlets.interfaces.IDashboard'],
            registered_interfaces
        )

    def test_interfaces(self):
        portlet = busca.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_addview(self):
        portlet = getUtility(IPortletType, name='brasil.gov.agenda.busca')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={
            'root': u'/'.join(self.agenda.getPhysicalPath())}
        )

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], busca.Assignment))

    def test_portlet_properties(self):
        portlet = getUtility(IPortletType, name='brasil.gov.agenda.busca')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={
            'root': u'/'.join(self.agenda.getPhysicalPath())}
        )
        title = mapping.values()[0].title
        root = mapping.values()[0].root
        self.assertEqual(title, u'Busca de Agenda')
        self.assertEqual(root, u'/'.join(self.agenda.getPhysicalPath()))

    def test_renderer(self):
        context = self.agenda
        request = self.agenda.REQUEST
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.agenda)
        assignment = busca.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, busca.Renderer))
        html = renderer.render()
        # Titulo do portlet
        self.assertIn('Busca de Agenda', html)
        # Id do texto explicativo
        self.assertIn('busca_agenda_texto', html)
