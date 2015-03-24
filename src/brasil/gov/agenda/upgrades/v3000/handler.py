# -*- coding: utf-8 -*-
from brasil.gov.agenda.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile
from zope.component.hooks import getSite

import logging


logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    """Atualiza perfil para versao 3000."""
    profile = 'profile-brasil.gov.agenda.upgrades.v3000:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 3000')


def fix_agendadiaria_catalog(context):
    """Atualiza catalog com Title e location."""
    site = getSite()
    ct = site.portal_catalog
    results = ct.searchResults(portal_type='AgendaDiaria')
    logger.info('Total de AgendasDiarias: %d' % len(results))
    i = 0
    for brain in results:
        obj = brain.getObject()
        obj.reindexObject(idxs=['Title', 'sortable_title', 'location'])
        i += 1

    logger.info('Total de Atualizadas: %d' % i)
