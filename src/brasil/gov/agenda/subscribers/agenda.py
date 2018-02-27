# -*- coding: utf-8 -*-
from plone.app.dexterity.behaviors.nextprevious import INextPreviousToggle


def habilita_next_previous(obj, event):
    """Ordenacao por id dentro de uma agenda."""
    behavior = INextPreviousToggle(obj)
    behavior.nextPreviousEnabled = True
