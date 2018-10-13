# -*- coding: utf-8 -*-
from brasil.gov.agenda.logger import logger
from plone import api


SWIPER_CSS = '//cdnjs.cloudflare.com/ajax/libs/Swiper/4.1.6/css/swiper.min.css'
SWIPER_JS = '//cdnjs.cloudflare.com/ajax/libs/Swiper/4.1.6/js/swiper.min.js'
OLD_CSS = '++resource++brasil.gov.agenda/agenda.css'
NEW_CSS = '++resource++brasil.gov.agenda/brasilgovagenda.css'
NEW_JS = '++resource++brasil.gov.agenda/brasilgovagenda.js'


def add_resource(tool, resource_id):
    if resource_id in tool.getResourceIds():
        return
    tool.registerResource(resource_id)
    tool.getResource(resource_id).setCompression('none')


def fix_resources_references(setup_tool):
    """Fix resource references."""
    css_tool = api.portal.get_tool('portal_css')
    add_resource(css_tool, SWIPER_CSS)
    css_tool.moveResourceBefore(SWIPER_CSS, '*')
    if OLD_CSS in css_tool.getResourceIds():
        css_tool.getResource(OLD_CSS).setCompression('none')
        css_tool.renameResource(OLD_CSS, NEW_CSS)
    js_tool = api.portal.get_tool('portal_javascripts')
    add_resource(js_tool, SWIPER_JS)
    js_tool.moveResourceBefore(SWIPER_JS, '*')
    add_resource(js_tool, NEW_JS)
    logger.info('Updated static resource references.')
