# -*- coding: utf-8 -*-
from brasil.gov.agenda.logger import logger
from plone import api


def uninstall_dependency(setup_tool):
    """Uninstall collective.portlet.calendar.
    https://github.com/plonegovbr/brasil.gov.agenda/issues/137
    """
    from collective.portlet.calendar.browser.interfaces import ICalendarExLayer
    from plone.browserlayer import utils
    logger.info('Removing collective.portlet.calendar')
    qi = api.portal.get_tool('portal_quickinstaller')
    pkg = 'collective.portlet.calendar'
    if qi.isProductInstalled(pkg):
        qi.uninstallProducts([pkg])
        logger.info(pkg + ' uninstalled')
    if ICalendarExLayer in utils.registered_layers():
        # XXX: we have to remove the layer using its name
        utils.unregister_layer('CalendarEx')
        logger.info(pkg + 'browser layer removed')
    logger.info('Done')
