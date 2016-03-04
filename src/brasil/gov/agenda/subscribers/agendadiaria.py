# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from brasil.gov.agenda.config import PROJECTNAME
from brasil.gov.agenda.interfaces import IAgendaDiaria
from five import grok
from zope.lifecycleevent.interfaces import IObjectAddedEvent

import datetime
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

    # Forcamos a data manualmente pois quando nao alterada
    # ele mantem o default_factory como valor padrao (o que muda todos os dias)
    date = [int(p) for p in obj.getId().split('-')]
    obj.date = datetime.date(*date)

    # Ordena objetos
    parent = aq_parent(obj)
    parent.orderObjects('id', reverse=False)
