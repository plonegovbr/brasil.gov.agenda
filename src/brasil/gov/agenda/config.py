# -*- coding: utf-8 -*-

from Products.CMFPlone import interfaces as plone_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implementer


PROJECTNAME = 'brasil.gov.agenda'

AGENDADIARIAFMT = '%Y-%m-%d'

TZ = 'Brazil/East'


@implementer(qi_interfaces.INonInstallable)
class HiddenProducts(object):

    def getNonInstallableProducts(self):
        return [
            'brasil.gov.agenda.upgrades.v2000',
            'brasil.gov.agenda.upgrades.v3000',
            'brasil.gov.agenda.upgrades.v4000',
            'brasil.gov.agenda.upgrades.v4001',
            'brasil.gov.agenda.upgrades.v4002',
            'brasil.gov.agenda.upgrades.v4003',
        ]


@implementer(plone_interfaces.INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.agenda:uninstall',
            u'brasil.gov.agenda.upgrades.v2000:default',
            u'brasil.gov.agenda.upgrades.v3000:default',
            u'brasil.gov.agenda.upgrades.v4000:default',
            u'collective.portlet.calendar:default',
            u'collective.portlet.calendar:uninstall'
        ]
