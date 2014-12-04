# -*- coding:utf-8 -*-
from brasil.gov.agenda.config import PROJECTNAME

import logging


logger = logging.getLogger(PROJECTNAME)


def corrige_campo_date_facetada(context):
    """Reindexa objetos para atualizar indices da data de
    publicacao
    """
    logger.info('Inicia atualizacao')
    ct = context.portal_catalog
    results = ct.searchResults(portal_type='AgendaDiaria')
    for brain in results:
        o = brain.getObject()
        o.reindexObject()
    logger.info('%d objetos corrigidos' % len(results))
