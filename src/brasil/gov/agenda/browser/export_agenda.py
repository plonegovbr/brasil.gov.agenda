# -*- coding: utf-8 -*-
"""Exportação de Agenda."""

from brasil.gov.agenda import _
from cStringIO import StringIO
from DateTime import DateTime
from dateutil.relativedelta import relativedelta
from plone import api
from plone.z3cform.layout import FormWrapper
from Products.Five.browser import BrowserView
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import WidgetActionExecutionError
from zope import interface
from zope import schema
from zope.interface import Invalid
from zope.schema.interfaces import RequiredMissing
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import csv


HEADER = [
    _(u'Schedule Title'),
    _(u'Schedule Description'),
    _(u'Department Name'),
    _(u'Authority Name'),
    _(u'Daily Schedule Date'),
    _(u'General information'),
    _(u'Appointment'),
    _(u'Appointment Location'),
    _(u'Start Time'),
    _(u'End Time'),
    _(u'Other attendees'),
    _(u'Appointment Agenda'),
]


STATES = SimpleVocabulary(
    [
        SimpleTerm(
            value=u'private',
            title=_(u'Private'),
        ),
        SimpleTerm(
            value=u'published',
            title=_(u'Published'),
        ),
    ],
)


class ExportAgendaFile(BrowserView):
    """View que retorna o arquivo csv com os compromissos da agenda."""

    def __init__(self, context, request):
        super(ExportAgendaFile, self).__init__(context, request)

        self.initial_date = None
        initial_date_str = self.request.get('initial_date', '')
        if initial_date_str:
            initial_date_format = '{0} 00:00:00'.format(initial_date_str)
            self.initial_date = DateTime(initial_date_format)

        self.final_date = None
        final_date_str = self.request.get('final_date', '')
        if final_date_str:
            final_date_format = '{0} 23:59:59'.format(final_date_str)
            self.final_date = DateTime(final_date_format)

        self.review_state = self.request.get('review_state', [])

    def get_compromissos(self):
        """Retorna os compromissos da Agenda entre as datas recebidas."""
        result = []
        date_range_query = {
            'query': (self.initial_date, self.final_date), 'range': 'min:max',
        }

        compromissos = api.content.find(
            self.context,
            portal_type='Compromisso',
            start=date_range_query,
        )
        compromissos_por_agenda_diaria = {}
        for compromisso in compromissos:
            path_agenda_diaria = '/'.join(
                compromisso.getPath().split('/')[:-1])
            if not compromissos_por_agenda_diaria.get(path_agenda_diaria, ''):
                compromissos_por_agenda_diaria[path_agenda_diaria] = []
            compromissos_por_agenda_diaria[path_agenda_diaria].append(
                compromisso)

        agendas_diarias = api.content.find(
            self.context,
            portal_type='AgendaDiaria',
            review_state=self.review_state,
            date=date_range_query,
            sort_on='date',
            sort_order='ascending',
        )
        for agenda_diaria in agendas_diarias:
            compromissos_agenda = compromissos_por_agenda_diaria.get(
                agenda_diaria.getPath(), [])
            obj_agenda_diaria = agenda_diaria.getObject()
            html = obj_agenda_diaria.update.output.encode(
                'utf-8') if obj_agenda_diaria.update else u''
            transforms = api.portal.get_tool('portal_transforms')
            stream = transforms.convertTo(
                'text/plain', html, mimetype='text/html')
            # converte o html para texto simples
            info = stream.getData().strip()
            # O formato da data foi definido pelo cliente
            dados_agenda_diaria = {'data_agenda': agenda_diaria.date.strftime('%d/%m/%Y'),
                                   'autoridade_agenda': agenda_diaria.autoridade,
                                   'local_agenda': agenda_diaria.location,
                                   'info': info}
            if not compromissos_agenda:
                result.append(dados_agenda_diaria)
            for compromisso in compromissos_agenda:
                retorno = dados_agenda_diaria.copy()
                retorno['compromisso'] = compromisso.Title
                retorno['autoridade_compromisso'] = compromisso.autoridade
                retorno['local_compromisso'] = compromisso.location
                retorno['pauta'] = compromisso.Description
                retorno['hora_inicio'] = compromisso.start.strftime('%H:%M')
                retorno['hora_fim'] = compromisso.end.strftime('%H:%M')
                retorno['participantes'] = ''
                if compromisso.attendees:
                    retorno['participantes'] = ', '.join(
                        compromisso.attendees.splitlines())
                result.append(retorno)
        return result

    def write_csv(self):
        """Cria o arquivo csv com os compromissos."""
        title_agenda = ''
        if self.context.title:
            title_agenda = self.context.title.encode('utf-8')
        orgao_agenda = ''
        if self.context.orgao:
            orgao_agenda = self.context.orgao.encode('utf-8')
        autoridade = ''
        if self.context.autoridade:
            autoridade = self.context.autoridade.encode('utf-8')
        description_agenda = ''
        if self.context.description:
            description_agenda = self.context.description.encode('utf-8')
        local = ''
        if self.context.location:
            local = self.context.location.encode('utf-8')

        out = StringIO()
        writer = csv.writer(out, quoting=csv.QUOTE_ALL)
        colunas = [self.context.translate(
            coluna).encode('utf-8') for coluna in HEADER]
        writer.writerow(colunas)

        compromissos = self.get_compromissos()
        for compromisso in compromissos:

            if compromisso.get('autoridade_compromisso', ''):
                autoridade = compromisso.get('autoridade_compromisso', '')
            elif compromisso.get('autoridade_agenda', ''):
                autoridade = compromisso.get('autoridade_agenda', '')

            if compromisso.get('local_compromisso', ''):
                local = compromisso.get('local_compromisso', '')
            elif compromisso.get('local_agenda', ''):
                local = compromisso.get('local_agenda', '')

            row = []
            if isinstance(title_agenda, unicode):
                title_agenda = title_agenda.encode('utf-8')
            row.append(title_agenda)

            if isinstance(description_agenda, unicode):
                description_agenda = description_agenda.encode('utf-8')
            row.append(description_agenda)

            if isinstance(orgao_agenda, unicode):
                orgao_agenda = orgao_agenda.encode('utf-8')
            row.append(orgao_agenda)

            if isinstance(autoridade, unicode):
                autoridade = autoridade.encode('utf-8')
            row.append(autoridade)

            data_agenda = compromisso.get('data_agenda', '')
            if isinstance(data_agenda, unicode):
                data_agenda = data_agenda.encode('utf-8')
            row.append(data_agenda)

            info = compromisso.get('info', '')
            if isinstance(info, unicode):
                info = info.encode('utf-8')
            row.append(info)

            txt = compromisso.get('compromisso', '')
            if isinstance(txt, unicode):
                txt = txt.encode('utf-8')
            row.append(txt)

            if isinstance(local, unicode):
                local = local.encode('utf-8')
            row.append(local)

            hora_inicio = compromisso.get('hora_inicio', '')
            if isinstance(hora_inicio, unicode):
                hora_inicio = hora_inicio.encode('utf-8')
            row.append(hora_inicio)

            hora_fim = compromisso.get('hora_fim', '')
            if isinstance(hora_fim, unicode):
                hora_fim = hora_fim.encode('utf-8')
            row.append(hora_fim)

            participantes = compromisso.get('participantes', '')
            if isinstance(participantes, unicode):
                participantes = participantes.encode('utf-8')
            row.append(participantes)

            pauta = compromisso.get('pauta', '')
            if isinstance(pauta, unicode):
                pauta = pauta.encode('utf-8')
            row.append(pauta)

            writer.writerow(row)

        return out.getvalue()

    def __call__(self):
        if not self.initial_date or not self.final_date or not self.review_state:
            return ''
        csv_file = self.write_csv()
        response = self.request.response
        self.request.response.setHeader('content-type', 'text/csv')
        response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}.csv"'.format(self.context.getId()),
        )
        return csv_file


def requiredConstraint(value):
    """A validação de obrigatoriedade padrão não funciona para o campo review_state."""

    if not value:
        raise RequiredMissing()
    return True


def valid_dates(initial_date, final_date):
    if initial_date is not None and final_date is not None:
        if initial_date > final_date:
            msg = _(u'Final date less than initial date')
            raise WidgetActionExecutionError('final_date', Invalid(msg))
        else:
            next_year = initial_date + relativedelta(years=1)
            if final_date > next_year:
                msg = _(
                    u'Final date greater than 1 year after the initial date')
                raise WidgetActionExecutionError(
                    'final_date', Invalid(msg))


class IExportAgendaForm(interface.Interface):

    initial_date = schema.Date(title=_(u'Initial Date'),
                               required=True)

    final_date = schema.Date(title=_(u'Final Date'),
                             required=True)

    review_state = schema.List(title=_(u'Daily Agenda Status'),
                               required=True,
                               constraint=requiredConstraint,
                               value_type=schema.Choice(vocabulary=STATES))


class ExportAgendaForm(form.Form):
    """Formulário de exportação de Agenda."""
    fields = field.Fields(IExportAgendaForm)
    fields['review_state'].widgetFactory = CheckBoxFieldWidget
    ignoreContext = True

    @button.buttonAndHandler(_(u'Export'), name='export')
    def handleExport(self, action):  # @UnusedVariable
        data, errors = self.extractData()
        initial_date = data.get('initial_date', None)
        final_date = data.get('final_date', None)
        valid_dates(initial_date, final_date)
        if errors:
            self.status = self.formErrorsMessage
            return

        review_state = data['review_state']
        context_url = self.context.absolute_url()
        state_url = ''
        for state in review_state:
            state_url += '&review_state={0}'.format(state.encode('utf-8'))
        self.request.RESPONSE.redirect(
            '{0}/export_agenda_file?initial_date={1}&final_date={2}{3}'.format(
                context_url, initial_date, final_date, state_url),
        )


class ExportAgendaFormWrapper(FormWrapper):
    """View do formulário de exportação de Compromissos da Agenda."""
    form = ExportAgendaForm
    label = _(u'Export Appointments')
