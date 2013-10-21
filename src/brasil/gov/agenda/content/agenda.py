# -*- coding: utf-8 -*-

from brasil.gov.agenda.interfaces import IAgenda
from five import grok
from plone.dexterity.content import Container


class Agenda(Container):
    """Agenda de um membro do Governo Brasileiro"""

    grok.implements(IAgenda)
