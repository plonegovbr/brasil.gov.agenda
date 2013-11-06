# -*- coding: utf-8 -*-

from brasil.gov.agenda import _
from brasil.gov.agenda.config import AGENDADIARIAFMT
from brasil.gov.agenda.interfaces import IAgenda
from brasil.gov.agenda.interfaces import IAgendaDiaria
from brasil.gov.agenda.interfaces import ICompromisso
from DateTime import DateTime
from five import grok
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.content import Container
from plone.directives import form
from plone.indexer.decorator import indexer
from plone.supermodel.interfaces import IDefaultFactory
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from z3c.form.validator import SimpleFieldValidator
from zope.interface import Invalid

import datetime


class AgendaDiaria(Container):
    """Agenda Diaria."""

    grok.implements(IAgendaDiaria)

    def Title(self):
        """ Retorna titulo calculado com autoridade e data
        """
        date = self.date
        fmt_date = date.strftime('%d/%m/%Y')
        autoridade = self.autoridade
        title = u'Agenda de %s para %s' % (autoridade, fmt_date)
        return title


@form.default_value(field=IExcludeFromNavigation['exclude_from_nav'])
def exclude_from_nav_default_value(data):
    # AgendaDiaria e Compromisso nao devem aparecer na navegacao
    context = data.context
    exclude = IAgenda.providedBy(context) or IAgendaDiaria.providedBy(context)
    return exclude


@provider(IContextAwareDefaultFactory)
def default_autoridade(context):
    """ Por padrao utilizamos a autoridade
        definida no objeto pai
    """
    return getattr(context, 'autoridade', u'')


@provider(IContextAwareDefaultFactory)
def default_location(context):
    return getattr(context, 'location', u'')


@provider(IDefaultFactory)
def default_date():
    """ Retorna um dia no futuro """
    return datetime.date.today() + datetime.timedelta(1)


class DateValidator(SimpleFieldValidator):
    def validate(self, value):
        """ Garantimos a unicidade das AgendasDiarias """
        super(DateValidator, self).validate(value)
        date = value.strftime(AGENDADIARIAFMT)
        oIds = self.context.objectIds()
        if date in oIds:
            raise Invalid(_(u'Ja existe uma agenda para esta data'))


@indexer(IAgendaDiaria)
def SearchableText_AgendaDiaria(obj):
    """ Indexa os dados dos compromissos dentro desta AgendaDiaria
        para prover busca por texto integral
    """
    children = obj.objectValues()
    SearchableText = []
    for child in children:
        if not ICompromisso.providedBy(child):
            continue
        # Campos indexaveis
        SearchableText.append(child.title)
        SearchableText.append(child.description)
        SearchableText.append(child.autoridade)
        SearchableText.append(child.location)
        SearchableText.append(child.attendees)
    if not SearchableText:
        SearchableText.append(obj.autoridade)
        SearchableText.append(obj.location)
    # Alteracao da agenda
    update = obj.update
    if hasattr(update, 'output'):
        update = update.output
    SearchableText.append(update)
    return ' '.join([text for text in SearchableText
                     if isinstance(text, basestring)])


@indexer(IAgendaDiaria)
def start_date(obj):
    """ Converte a data da AgendaDiaria para DateTime e coloca o
        horario como 00:00:00
    """
    start_date = IAgendaDiaria(obj).date
    # Comeco do dia
    start_date = DateTime('%s 00:00:00' % start_date.strftime('%Y-%m-%d'))
    return start_date


@indexer(IAgendaDiaria)
def end_date(obj):
    """ Converte a data da AgendaDiaria para DateTime e coloca o
        horario como 23:59:59
    """
    end_date = IAgendaDiaria(obj).date
    # Final do dia
    end_date = DateTime('%s 23:59:59' % end_date.strftime('%Y-%m-%d'))

    return end_date
