# -*- coding: utf-8 -*-
from brasil.gov.agenda.logger import logger
from plone import api


OLD_CSS = '++resource++brasil.gov.agenda/agenda.css'


def fix_resources_references(setup_tool):
    """Fix resource references."""
    css_tool = api.portal.get_tool('portal_css')
    if OLD_CSS in css_tool.getResourceIds():
        css_tool.unregisterResource(OLD_CSS)
    logger.info('Updated static resource references.')
