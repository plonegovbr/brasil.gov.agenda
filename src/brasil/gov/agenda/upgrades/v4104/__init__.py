# -*- coding: utf-8 -*-
from brasil.gov.agenda.logger import logger
from plone import api


SCRIPTS = [
    '//cdnjs.cloudflare.com/ajax/libs/Swiper/4.1.6/js/swiper.min.js',
    '++resource++brasil.gov.agenda/brasilgovagenda.js',
]
STYLES = [
    '//cdnjs.cloudflare.com/ajax/libs/Swiper/4.1.6/css/swiper.min.css',
    '++resource++brasil.gov.agenda/brasilgovagenda.css',
]


def deprecate_resource_registries(setup_tool):
    """Deprecate resource registries."""
    js_tool = api.portal.get_tool('portal_javascripts')
    for js in SCRIPTS:
        if js not in js_tool.getResourceIds():
            continue
        js_tool.unregisterResource(id=js)
        assert js not in js_tool.getResourceIds()  # nosec

    css_tool = api.portal.get_tool('portal_css')
    for css in STYLES:
        if css not in css_tool.getResourceIds():
            continue
        css_tool.unregisterResource(id=css)
        assert css not in css_tool.getResourceIds()  # nosec

    logger.info('Static resources successfully removed from registries')
