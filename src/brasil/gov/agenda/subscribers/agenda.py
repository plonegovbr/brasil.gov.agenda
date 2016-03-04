# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import PROJECTNAME
from brasil.gov.agenda.interfaces import IAgenda
from five import grok
from plone.app.dexterity.behaviors.nextprevious import INextPreviousToggle
from zope.lifecycleevent.interfaces import IObjectAddedEvent

import logging


logger = logging.getLogger(PROJECTNAME)


@grok.subscribe(IObjectAddedEvent)
def habilita_next_previous(event, obj=None):
    """ Ordenacao por id dentro de uma agenda
    """
    if not obj:
        obj = event.object

    if not IAgenda.providedBy(obj):  # nao eh uma agenda
        return

    behavior = INextPreviousToggle(obj)
    behavior.nextPreviousEnabled = True
