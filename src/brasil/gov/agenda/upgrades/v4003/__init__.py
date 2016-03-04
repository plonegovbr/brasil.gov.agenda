# -*- coding: utf-8 -*-

from brasil.gov.agenda.logger import logger
from plone import api


def cook_css_resources(context):
    """Cook CSS resources."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.cookResources()
    logger.info('CSS resources were cooked')


def make_content_types_linkable(context):
    """Add package content types to the list of linkables on TinyMCE."""
    tinymce = api.portal.get_tool('portal_tinymce')
    linkable = tinymce.linkable.split()
    for t in ('Agenda', 'AgendaDiaria', 'Compromisso'):
        if t not in linkable:
            linkable.append(t)
            tinymce.linkable = u'\n'.join(linkable)
            logger.info('{0} added to linkable types in TinyMCE.'.format(t))


def update_effective_date_index(context):
    """Reindex existing AgendaDiaria objects to fix EffectiveDate metadata."""
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type='AgendaDiaria')
    for brain in results:
        o = brain.getObject()
        o.reindexObject(idxs=['EffectiveDate'])
    logger.info('{0} objects reindexed'.format(len(results)))
