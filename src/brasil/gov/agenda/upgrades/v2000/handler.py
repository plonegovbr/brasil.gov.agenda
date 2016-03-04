# -*- coding: utf-8 -*-
from brasil.gov.agenda.config import PROJECTNAME
from plone.app.textfield.value import RichTextValue
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFPlone.utils import safe_hasattr
from zope.component.hooks import getSite

import logging


logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    """Atualiza perfil para versao 2000."""
    profile = 'profile-brasil.gov.agenda.upgrades.v2000:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 2000')


def fix_agendadiaria_update(context):
    """Atualiza campo update da AgendaDiaria."""
    site = getSite()
    ct = site.portal_catalog
    results = ct.searchResults(portal_type='AgendaDiaria')
    logger.info('Total de AgendasDiarias: %d' % len(results))
    i = 0
    for brain in results:
        obj = brain.getObject()
        update = u'' if not obj.update else obj.update

        if safe_hasattr(update, 'raw'):
            continue
        update = update.replace('\n', '<br />')
        # Cria o valor RichText
        value = RichTextValue(update,
                              'text/html',
                              'text/x-html-safe',
                              encoding='utf-8')
        # Atualiza o objeto
        obj.update = value
        i += 1

    logger.info('Total de Atualizadas: %d' % i)
