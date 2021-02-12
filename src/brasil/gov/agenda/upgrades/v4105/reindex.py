# -*- coding: utf-8 -*-
from brasil.gov.agenda.setuphandlers import setup_catalog
from plone import api

import transaction


def reindex_catalog(context):
    """ Cria e reindexa o indice date e os metadados autoridade, update e attendees
        Segue orientação:
        https://community.plone.org/t/best-practices-on-reindexing-the-catalog/4157/14
    """
    setup_catalog(context)
    catalog = api.portal.get_tool('portal_catalog')

    # Agendas diárias
    n = 0
    agendas = catalog(portal_type='AgendaDiaria')
    for agenda in agendas:
        obj_agenda = agenda.getObject()
        catalog.catalog_object(obj_agenda, idxs=['date'], update_metadata=True)
        n += 1
        if n % 1000 == 0:
            transaction.commit()

    # Compromissos
    n = 0
    compromissos = catalog(portal_type='Compromisso')
    for compromisso in compromissos:
        obj_compromisso = compromisso.getObject()
        catalog.catalog_object(obj_compromisso, idxs=[], update_metadata=True)
        n += 1
        if n % 1000 == 0:
            transaction.commit()
