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
