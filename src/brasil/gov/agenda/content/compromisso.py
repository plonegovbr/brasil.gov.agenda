# -*- coding: utf-8 -*-

from brasil.gov.agenda.interfaces import IAgendaDiaria
from brasil.gov.agenda.interfaces import ICompromisso
from DateTime import DateTime
from five import grok
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.content import Container
from plone.directives import form
from plone.indexer.decorator import indexer
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

import datetime


class Compromisso(Container):
    """Compromisso."""

    grok.implements(ICompromisso)


@form.default_value(field=IExcludeFromNavigation['exclude_from_nav'],
                    context=IAgendaDiaria)
def exclude_from_nav_default_value(data):
    return True


@provider(IContextAwareDefaultFactory)
def default_autoridade(context):
    return getattr(context, 'autoridade', u'')


@provider(IContextAwareDefaultFactory)
def default_location(context):
    return getattr(context, 'location', u'')


@provider(IContextAwareDefaultFactory)
def default_start_date(context):
    if IAgendaDiaria.providedBy(context):
        date = context.date
        default_date = datetime.datetime(
            *[int(i) for i in date.strftime('%Y-%m-%d').split('-')]
        )
    else:
        # Estamos no tipo agenda, a data padrao e o dia seguinte a criacao
        # do compromisso
        default_date = datetime.datetime.today() + datetime.timedelta(1)
    return default_date


@provider(IContextAwareDefaultFactory)
def default_end_date(context):
    if IAgendaDiaria.providedBy(context):
        # Estamos em uma agenda diaria, a data padrao e a da
        # agenda
        date = context.date
        default_date = datetime.datetime(
            *[int(i) for i in date.strftime('%Y-%m-%d').split('-')]
        )
    else:
        # Estamos no tipo agenda, a data padrao e o dia seguinte a criacao
        # do compromisso + 60 minutos
        default_date = datetime.datetime.today() + datetime.timedelta(1, 3600)
    return default_date


@indexer(ICompromisso)
def start_date(obj):
    return DateTime(ICompromisso(obj).start_date)


@indexer(ICompromisso)
def end_date(obj):
    return DateTime(ICompromisso(obj).end_date)
