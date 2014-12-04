# -*- coding:utf-8 -*-
from brasil.gov.agenda.logger import logger
from plone import api


def make_agenda_linkable_on_tinymce(context):
    """Add Agenda to the list of linkable content types on TinyMCE."""
    tinymce = api.portal.get_tool('portal_tinymce')
    linkable = tinymce.linkable.split()
    if 'Agenda' not in linkable:
        linkable.append('Agenda')
        tinymce.linkable = u'\n'.join(linkable)
        logger.info('Agenda added to linkable types in TinyMCE.')


def update_effective_date_index(context):
    """Reindex existing AgendaDiaria objects to fix EffectiveDate metadata."""
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type='AgendaDiaria')
    for brain in results:
        o = brain.getObject()
        o.reindexObject(idxs=['EffectiveDate'])
    logger.info('{:d} objects reindexed'.format(len(results)))
