# -*- coding: utf-8 -*-
from brasil.gov.agenda.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    """Atualiza perfil para versao 4000."""
    profile = 'profile-brasil.gov.agenda.upgrades.v4000:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 4000')
