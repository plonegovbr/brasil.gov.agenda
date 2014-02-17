# -*- coding:utf-8 -*-
from Products.CMFPlone import interfaces as plone_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implements

PROJECTNAME = "brasil.gov.agenda"

AGENDADIARIAFMT = '%Y-%m-%d'


class HiddenProducts(object):

    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        return [
            'brasil.gov.agenda.upgrades.v2000'
            'brasil.gov.agenda.upgrades.v3000'
            'brasil.gov.agenda.upgrades.v4000'
            'brasil.gov.agenda.upgrades.v4001'
        ]


class HiddenProfiles(object):
    implements(plone_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.agenda:uninstall',
            u'brasil.gov.agenda.upgrades.v2000:default'
            u'brasil.gov.agenda.upgrades.v3000:default'
            u'brasil.gov.agenda.upgrades.v4000:default'
            u'collective.portlet.calendar:default'
            u'collective.portlet.calendar:uninstall'
        ]
