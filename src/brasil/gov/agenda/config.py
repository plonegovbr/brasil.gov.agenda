# -*- coding:utf-8 -*-
from Products.CMFPlone import interfaces as plone_interfaces
from zope.interface import implements

PROJECTNAME = "brasil.gov.agenda"

AGENDADIARIAFMT = '%Y-%m-%d'


class HiddenProfiles(object):
    implements(plone_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.agenda:uninstall',
            u'brasil.gov.agenda.upgrades.v2000:default'
            u'collective.portlet.calendar:default'
            u'collective.portlet.calendar:uninstall'
        ]
