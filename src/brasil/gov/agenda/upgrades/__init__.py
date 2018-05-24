# -*- coding: utf-8 -*-
from brasil.gov.agenda.logger import logger
from plone import api


def cook_css_resources(context):
    """Cook CSS resources."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.cookResources()
    logger.info('CSS resources were cooked')


def cook_javascript_resources(context):
    """Cook JavaScript resources."""
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.cookResources()
    logger.info('JavaScript resources were cooked')


def get_valid_objects(brains):
    """Generate a list of objects associated with valid brains."""
    for b in brains:
        try:
            obj = b.getObject()
        except (AttributeError, KeyError):
            obj = None

        if obj is None:  # warn on broken entries in the catalog
            logger.warn(
                u'Invalid reference in the catalog: {0}'.format(b.getPath()))
            continue
        yield obj
