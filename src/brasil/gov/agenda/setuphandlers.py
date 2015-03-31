# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


def list_agendadiaria_calendar(p):
    """ Listaremos o tipo AgendaDiaria no calendario do site """
    calendar = getToolByName(p, 'portal_calendar', None)
    if calendar is not None:
        our_type = 'AgendaDiaria'
        types = list(calendar.calendar_types)
        if our_type not in types:
            types.append(our_type)
            calendar.calendar_types = tuple(types)


def setup_site(context):
    """ Ajustamos o site para receber o produto de agenda
    """
    # Executado apenas se o estivermos no Profile correto
    if context.readDataFile('brasil.gov.agenda.txt') is None:
        return
    site = context.getSite()
    list_agendadiaria_calendar(site)
