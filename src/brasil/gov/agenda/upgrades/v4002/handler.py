# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import PROJECTNAME
from plone import api

import logging


logger = logging.getLogger(PROJECTNAME)


def remove_behavior_agendadiaria_compromisso(context):
    """Removemos o behavior IExcludeFromNav dos tipos
       AgendaDiaria e Compromisso
    """
    types_tool = api.portal.get_tool('portal_types')
    behavior = 'plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation'
    types = ['AgendaDiaria', 'Compromisso']
    for pt in types:
        obj = types_tool[pt]
        behaviors = list(obj.behaviors)
        if behavior in behaviors:
            behaviors.remove(behavior)
            obj.behaviors = tuple(behaviors)
            logger.info('Removido IExcludeFromNavigation do tipo {0}'.format(pt))


def metaTypesNotToList_agendadiaria_compromisso(context):
    """Os tipos AgendaDiaria e Compromisso sao adicionados
       a lista metaTypesNotToList (ocultando-os de portlets de navegacao)
    """
    navtree_properties = api.portal.get_tool('portal_properties')['navtree_properties']
    metaTypesNotToList = list(navtree_properties.metaTypesNotToList)
    types = ['AgendaDiaria', 'Compromisso']

    for pt in types:
        if pt not in metaTypesNotToList:
            metaTypesNotToList.append(pt)
    navtree_properties._updateProperty('metaTypesNotToList', metaTypesNotToList)
    logger.info('Tipos adicionados a metaTypesNotToList')


def aplica_behavior_agenda(context):
    """Aplicamos o behavior IExcludeFromNav no tipo Agenda
    """
    types_tool = api.portal.get_tool('portal_types')
    behavior = 'plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation'
    types = ['Agenda', ]
    for pt in types:
        obj = types_tool[pt]
        behaviors = list(obj.behaviors)
        if behavior not in behaviors:
            behaviors.append(behavior)
            obj.behaviors = tuple(behaviors)
            logger.info('Aplicado IExcludeFromNavigation no tipo {0}'.format(pt))


def atualiza_exclude_from_nav(context):
    """Atualizamos o metadado exclude_from_nav dos tipos
       AgendaDiaria e Compromisso
    """
    ct = api.portal.get_tool('portal_catalog')
    types = ['AgendaDiaria', 'Compromisso']
    results = ct.unrestrictedSearchResults(portal_type=types)
    logger.info('Atualizacao de exclude_from_nav: {0} itens'.format(len(results)))
    for b in results:
        if b.exclude_from_nav:
            continue
        obj = b.getObject()
        # Reindexamos apenas o indice Type para evitar uma alteracao na
        # data de modificacao. Metadados sao sempre atualizados
        obj.reindexObject(idxs=['Type'])
    logger.info('Atualizacao do exclude_from_nav completa')
