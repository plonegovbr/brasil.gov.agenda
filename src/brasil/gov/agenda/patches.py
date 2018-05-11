# -*- coding: utf-8 -*-

from brasil.gov.agenda.logger import logger
from plone.app.portlets import utils
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.portlets.storage import UserPortletAssignmentMapping
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.constants import USER_CATEGORY
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import getUtility


def assignment_mapping_from_key():
    # Customização obtida de
    # https://github.com/plone/plone.app.portlets/blob/2.5.6/plone/app/portlets/utils.py#L55
    def patched_assignment_mapping_from_key(context, manager_name, category, key, create=False):
        """Given the name of a portlet manager, the name of a category, and a
        key in that category, return the IPortletAssignmentMapping.
        Raise a KeyError if it cannot be found.
        """
        manager = getUtility(IPortletManager, manager_name)

        if category == CONTEXT_CATEGORY:
            path = key
            portal = getToolByName(context, 'portal_url').getPortalObject()
            portal_path = '/'.join(portal.getPhysicalPath())
            if path == portal_path:
                # there may be problem if PloneSite id is 'plone'.
                # restrictedTraverse traverses to @@plone BrowserView which
                # is wrong
                obj = portal
            else:
                if path.startswith(portal_path + '/'):
                    path = path[len(portal_path)+1:]  # NOQA
                while path.startswith('/'):
                    path = path[1:]
                # INICIO CUSTOMIZAÇÃO
                obj = portal.restrictedTraverse(str(path), None)
                # FIM CUSTOMIZAÇÃO
            if obj is None:
                raise KeyError, "Cannot find object at path %s" % path  # NOQA
            return getMultiAdapter((obj, manager), IPortletAssignmentMapping)
        else:
            mapping = manager[category]
            if key not in mapping and create:
                if category == USER_CATEGORY:
                    mapping[key] = UserPortletAssignmentMapping()
                else:
                    mapping[key] = PortletAssignmentMapping()
            return mapping[key]

    setattr(utils, 'assignment_mapping_from_key', patched_assignment_mapping_from_key)
    logger.info('Patched plone.app.portlets.utils.assignment_mapping_from_key')


def run():
    assignment_mapping_from_key()
