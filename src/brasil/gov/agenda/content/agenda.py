# -*- coding: utf-8 -*-

from brasil.gov.agenda.interfaces import IAgenda
from five import grok
from plone.dexterity.content import Container
from plone.directives import form
from plone.app.dexterity.behaviors.nextprevious import INextPreviousToggle


class Agenda(Container):
    """Agenda de um membro do Governo Brasileiro"""

    grok.implements(IAgenda)


@form.default_value(field=INextPreviousToggle['nextPreviousEnabled'])
def next_previous_default_value(data):
    # A unica forma de descobrirmos se estamos sendo chamados pelo form
    # de Agenda eh olharmos a URL
    is_agenda = data.request.URL.endswith('++add++Agenda')
    return is_agenda
