# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool import interfaces as BBB
from zope.interface import implementer


@implementer(BBB.INonInstallable)  # BBB: Plone 4.3
@implementer(INonInstallable)
class NonInstallable(object):  # pragma: no cover

    @staticmethod
    def getNonInstallableProducts():
        """Hide in the add-ons configlet."""
        return [
            u'brasil.gov.agenda.upgrades.v4101',
            u'brasil.gov.agenda.upgrades.v4102',
            u'brasil.gov.agenda.upgrades.v4103',
            u'brasil.gov.agenda.upgrades.v4104',
            u'brasil.gov.agenda.upgrades.v4105',
            u'brasil.gov.agenda.upgrades.v4106',
            # BBB: https://github.com/plonegovbr/brasil.gov.agenda/issues/137
            u'collective.portlet.calendar',
        ]

    @staticmethod
    def getNonInstallableProfiles():
        """Hide at site creation."""
        return [
            u'brasil.gov.agenda:uninstall',
            u'brasil.gov.agenda.upgrades.v4101:default',
            u'brasil.gov.agenda.upgrades.v4104:default',
            # BBB: https://github.com/plonegovbr/brasil.gov.agenda/issues/137
            u'collective.portlet.calendar:default',
            u'collective.portlet.calendar:uninstall',
        ]


def list_agendadiaria_calendar(p):
    """ Listaremos o tipo AgendaDiaria no calendario do site """
    calendar = api.portal.get_tool('portal_calendar')
    if calendar is not None:
        our_type = 'AgendaDiaria'
        types = list(calendar.calendar_types)
        if our_type not in types:
            types.append(our_type)
            calendar.calendar_types = tuple(types)


def setup_catalog(portal):
    """ Cria indice e metadados no catalog.
    Foi feito aqui em vez de em profiles/default/catalog.xml para que
    não precise reindexar esses índices após cada reinstalação.
    https://docs.plone.org/develop/plone/searching_and_indexing/indexing.html#adding-index-using-add-on-product-installer
    """
    catalog = api.portal.get_tool('portal_catalog')

    if 'date' not in catalog.indexes():
        catalog.addIndex('date', 'DateIndex')

    metadatas = ['date', 'autoridade', 'attendees']

    idsMetadatas = catalog.schema()

    for metadata in metadatas:
        if metadata not in idsMetadatas:
            catalog.addColumn(metadata)


def setup_site(context):
    """ Ajustamos o site para receber o produto de agenda
    """
    # Executado apenas se o estivermos no Profile correto
    if context.readDataFile('brasil.gov.agenda.txt') is None:
        return
    site = context.getSite()
    list_agendadiaria_calendar(site)
    setup_catalog(site)
