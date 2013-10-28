# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from brasil.gov.agenda.interfaces import IAgendaDiaria
from brasil.gov.agenda.config import PROJECTNAME
from five import grok
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from zope.lifecycleevent.interfaces import IObjectAddedEvent

import logging

logger = logging.getLogger(PROJECTNAME)


@grok.subscribe(IObjectAddedEvent)
def ordenacao_agenda(event, obj=None):
    """ Ordenacao por id dentro de uma agenda
    """
    if not obj:
        obj = event.object

    if not IAgendaDiaria.providedBy(obj):  # nao eh uma agenda
        return

    # Exclui da navegacao
    behavior = IExcludeFromNavigation(obj)
    behavior.exclude_from_nav = True

    parent = aq_parent(obj)
    parent.orderObjects('id', reverse=False)
