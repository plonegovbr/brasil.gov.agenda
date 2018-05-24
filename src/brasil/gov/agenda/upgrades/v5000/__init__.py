# -*- coding: utf-8 -*-
from brasil.gov.agenda.logger import logger
from brasil.gov.agenda.upgrades import get_valid_objects
from plone import api

import transaction


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


def fix_subjects_on_agendas(setup_tool):
    """Fix None subjects on agendas.
    Refs. https://github.com/plonegovbr/brasil.gov.agenda/issues/85
    """
    test = 'test' in setup_tool.REQUEST  # used to ignore transactions on tests
    logger.info('Reindexing the catalog')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type='Agenda')
    logger.info(u'Found {0} agendas'.format(len(results)))
    n = 0
    for obj in get_valid_objects(results):
        if obj.subjects is not None:
            continue

        obj.subjects = ()
        catalog.catalog_object(obj, idxs=['Subject'])
        n += 1
        if n % 1000 == 0 and not test:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    if not test:
        transaction.commit()
    logger.info('Done.')
