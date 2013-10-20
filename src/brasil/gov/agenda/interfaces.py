# -*- coding: utf-8 -*-

from zope.interface import Interface


class IBrowserLayer(Interface):
    """Layer especifico para este add-on.

    Esta interface e referenciada em browserlayers.xml.

    Views e viewlets registrados para este layer serao exibidos
    apenas quando o produto estiver instalado.
    """


class IAgenda(Interface):
    """Schema do tipo de conteúdo Agenda."""


class IAgendaDiaria(Interface):
    """Schema do tipo de conteúdo Agenda."""


class ICompromisso(Interface):
    """Schema do tipo de conteúdo Compromisso."""
