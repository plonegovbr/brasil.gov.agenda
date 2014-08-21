# -*- coding: utf-8 -*-
from brasil.gov.agenda.interfaces import IAgenda
from five import grok
from plone.dexterity.content import Container
from plone.indexer.decorator import indexer


class Agenda(Container):
    """Agenda de um membro do Governo Brasileiro"""

    grok.implements(IAgenda)


@indexer(IAgenda)
def tags(obj):
    """Indexa tags de Agenda
    """
    tags = obj.subjects
    return tags
