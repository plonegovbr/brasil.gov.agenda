# -*- coding: utf-8 -*-
from brasil.gov.agenda import _
from brasil.gov.agenda import utils
from brasil.gov.agenda.config import AGENDADIARIAFMT
from brasil.gov.agenda.config import TZ
from brasil.gov.agenda.interfaces import IAgendaDiaria
from brasil.gov.agenda.interfaces import ICompromisso
from DateTime import DateTime
from five import grok
from plone import api
from plone.dexterity.content import Container
from plone.indexer.decorator import indexer
from plone.supermodel.interfaces import IDefaultFactory
from z3c.form.validator import SimpleFieldValidator
from zope.interface import Invalid
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


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

    def exclude_from_nav(self):
        """ AgendaDiaria nao eh visivel na navegacao do portal
        """
        return True

    @property
    def effective_date(self):
        """ Metodo que retorna
        """
        # Usamos a logica do indexer para start_date
        date = _start_date(self)
        if not date.isPast():
            # Se estiver no futuro, data de efetivacao sera agora
            now = DateTime()
            return now
        return date


@provider(IContextAwareDefaultFactory)
def default_autoridade(context):
    """ Por padrao utilizamos a autoridade
        definida no objeto pai
    """
    return getattr(context, 'autoridade', u'')


@provider(IContextAwareDefaultFactory)
def default_location(context):
    return getattr(context, 'location', u'')


@provider(IContextAwareDefaultFactory)
def default_subjects(context):
    return getattr(context, 'subjects', ())


@provider(IDefaultFactory)
def default_date():
    """ Retorna um dia no futuro """
    return utils.tomorrow()


class DateValidator(SimpleFieldValidator):
    def validate(self, value):
        """ Garantimos a unicidade das AgendasDiarias """
        super(DateValidator, self).validate(value)
        date = value.strftime(AGENDADIARIAFMT)
        oIds = self.context.objectIds()
        if date in oIds:
            raise Invalid(_(u'Ja existe uma agenda para esta data'))


@indexer(IAgendaDiaria)
def tags(obj):
    """Indexa tags de AgendaDiaria
    """
    tags = obj.subjects
    return tags


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


def _start_date(obj):
    """ Converte a data da AgendaDiaria para DateTime e coloca o
        horario como 00:00:00
    """
    start_date = IAgendaDiaria(obj).date
    # Comeco do dia
    start_date = DateTime(
        '{0} 00:00:00 {1}'.format(
            start_date.strftime('%Y-%m-%d'),
            TZ
        )
    )
    return start_date


@indexer(IAgendaDiaria)
def start_date(obj):
    """ Indexa a data de inicio com base na logica existente em _start_date
    """
    return _start_date(obj)


@indexer(IAgendaDiaria)
def end_date(obj):
    """ Converte a data da AgendaDiaria para DateTime e coloca o
        horario como 23:59:59
    """
    end_date = IAgendaDiaria(obj).date
    # Final do dia
    end_date = DateTime(
        '{0} 23:59:59 {1}'.format(
            end_date.strftime('%Y-%m-%d'),
            TZ
        )
    )
    return end_date


@indexer(IAgendaDiaria)
def exclude_from_nav(obj):
    # Agendas Diarias sempre serao ocultas da navegacao
    exclude_from_nav = obj.exclude_from_nav
    if hasattr(exclude_from_nav, '__call__'):
        exclude_from_nav = exclude_from_nav()
    return exclude_from_nav


@indexer(IAgendaDiaria)
def EffectiveDate(obj):
    """Retorna a data de inicio do evento ao invés da data de publicação para
    objetos publicados.
    """
    state = api.content.get_state(obj=obj)
    if state == 'published':
        return _start_date(obj).ISO()
    effective_date = IAgendaDiaria(obj).effective_date.ISO()
    return effective_date
