# -*- coding: utf-8 -*-
from brasil.gov.agenda.logger import logger
from brasil.gov.agenda.upgrades import get_valid_objects
from plone import api

import transaction


def fix_subjects_on_agendas(setup_tool):
    """Fix None subjects on agendas.
    Refs. https://github.com/plonegovbr/brasil.gov.agenda/issues/85
    """
    test = 'test' in setup_tool.REQUEST  # used to ignore transactions on tests
    logger.info('Fixing subject field values in agendas')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type=['Agenda', 'AgendaDiaria', 'Compromisso'])
    logger.info('{0} items will be analyzed'.format(len(results)))
    n = 0
    for obj in get_valid_objects(results):
        if obj.subjects is None:
            obj.subjects = ()

        catalog.catalog_object(obj)
        n += 1
        if n % 1000 == 0 and not test:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    if not test:
        transaction.commit()
    logger.info('Done.')
