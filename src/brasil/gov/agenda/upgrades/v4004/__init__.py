# -*- coding: utf-8 -*-
from brasil.gov.agenda.logger import logger
from plone import api


OLD_CSS = '++resource++brasil.gov.agenda/agenda.css'
NEW_CSS = '++resource++brasil.gov.agenda/brasilgovagenda.css'
NEW_JS = '++resource++brasil.gov.agenda/brasilgovagenda.js'


def fix_resources_references(setup_tool):
    """Fix resource references."""
    css_tool = api.portal.get_tool('portal_css')
    if OLD_CSS in css_tool.getResourceIds():
        css_tool.getResource(OLD_CSS).setCompression('none')
        css_tool.renameResource(OLD_CSS, NEW_CSS)
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.registerResource(NEW_JS)
    js_tool.getResource(NEW_JS).setCompression('none')
    logger.info('Updated static resource references.')
