# -*- coding: utf-8 -*-
from brasil.gov.agenda.logger import logger
from plone import api


SWIPER_CSS = '//cdnjs.cloudflare.com/ajax/libs/Swiper/4.1.6/css/swiper.min.css'
SWIPER_JS = '//cdnjs.cloudflare.com/ajax/libs/Swiper/4.1.6/js/swiper.min.js'
OLD_CSS = '++resource++brasil.gov.agenda/agenda.css'
NEW_CSS = '++resource++brasil.gov.agenda/brasilgovagenda.css'
NEW_JS = '++resource++brasil.gov.agenda/brasilgovagenda.js'


def fix_resources_references(setup_tool):
    """Fix resource references."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.registerResource(SWIPER_CSS)
    res = css_tool.getResource(SWIPER_CSS)
    res.setCompression('none')
    css_tool.moveResourceBefore(res, '*')
    if OLD_CSS in css_tool.getResourceIds():
        css_tool.getResource(OLD_CSS).setCompression('none')
        css_tool.renameResource(OLD_CSS, NEW_CSS)
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.registerResource(SWIPER_JS)
    res = js_tool.getResource(SWIPER_JS)
    res.setCompression('none')
    js_tool.moveResourceBefore(res, '*')
    js_tool.registerResource(NEW_JS)
    js_tool.getResource(NEW_JS).setCompression('none')
    logger.info('Updated static resource references.')
