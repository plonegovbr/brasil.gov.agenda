# -*- coding: utf-8 -*-
from brasil.gov.agenda.interfaces import IAgenda
from plone.dexterity.content import Container
from plone.dexterity.utils import safe_utf8
from plone.indexer.decorator import indexer
from zope.interface import implementer


@implementer(IAgenda)
class Agenda(Container):
    """Agenda de um membro do Governo Brasileiro"""


@indexer(IAgenda)
def tags(obj):
    """Indexa tags de Agenda."""
    if obj.subjects is None:
        return ()
    return tuple(safe_utf8(s) for s in obj.subjects)
