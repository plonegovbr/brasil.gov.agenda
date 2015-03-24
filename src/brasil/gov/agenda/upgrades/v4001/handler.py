# -*- coding: utf-8 -*-
from brasil.gov.agenda import utils
from brasil.gov.agenda.config import PROJECTNAME

import datetime
import logging


logger = logging.getLogger(PROJECTNAME)


def corrige_campo_date(context):
    """Utilizando como base o id do objeto, atualizamos os campos date
       quando o mesmo ainda utilizar o default_factory
    """
    logger.info('Inicia atualizacao')
    amanha = utils.tomorrow()
    ct = context.portal_catalog
    results = ct.searchResults(portal_type='AgendaDiaria')
    logger.info('%d objetos do tipo AgendaDiaria' % len(results))
    corrigidas = []
    for brain in results:
        o = brain.getObject()
        oId = o.getId()
        date = getattr(o, 'date', amanha)
        if not (date.strftime('%Y-%m-%d') == oId):
            # AgendaDiaria precisa ser corrigida
            # Setaremos o campo date com o valor do id do objeto
            date = datetime.date(*[int(p) for p in oId.split('-')])
            o.date = date
            o.reindexObject()
            corrigidas.append(oId)
    logger.info('%d objetos corrigidos' % len(corrigidas))
