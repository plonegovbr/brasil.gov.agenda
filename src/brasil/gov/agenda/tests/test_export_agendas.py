# -*- coding: utf-8 -*-
"""Testes da exportação de Agendas."""

from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue

import datetime
import unittest


class TestExportAgendaFile(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Site Administrator'])
        ltool = api.portal.get_tool('portal_languages')
        ltool.setLanguageBindings()
        self.agenda = api.content.create(
            self.portal,
            'Agenda',
            'agenda',
            u'Agenda de Autoridade',
            description=u'Agenda de José',
            orgao=u'Órgão de José',
            autoridade=u'José',
            location=u'Local',
            update=RichTextValue(u'Atualização',
                                 'text/html',
                                 'text/x-html-safe',
                                 encoding='utf-8'),
        )
        agenda_diariaPublica = api.content.create(
            self.agenda, 'AgendaDiaria', '2019-12-01')
        api.content.transition(obj=agenda_diariaPublica, transition='publish')
        agenda_diariaPrivada = api.content.create(
            self.agenda, 'AgendaDiaria', '2019-12-25')
        api.content.create(
            agenda_diariaPublica,
            'Compromisso',
            'compromisso01',
            u'Compromisso 01',
            start_date=datetime.datetime(2019, 12, 1, 12, 0),
            end_date=datetime.datetime(2019, 12, 1, 13, 0),
            description=u'Pauta 01',
            attendees=u'Maria',
        )
        api.content.create(
            agenda_diariaPrivada,
            'Compromisso',
            'compromisso25',
            u'Compromisso 25',
            start_date=datetime.datetime(2019, 12, 25, 8, 0),
            end_date=datetime.datetime(2019, 12, 25, 9, 0),
            description=u'Pauta 25',
            attendees=u'Marta',
        )

    def test_file_without_date_and_state(self):
        """Testa o arquivo quando não são passadas datas e estado."""
        view = api.content.get_view(
            'export_agenda_file', self.agenda, self.request)
        self.assertFalse(view())

    def test_get_compromissos_all(self):
        """Testa get_compromissos retornando todos os Compromissos."""
        self.request.set('initial_date', '2019-01-01')
        self.request.set('final_date', '2019-12-25')
        self.request.set('review_state', ['private', 'published'])
        view = api.content.get_view(
            'export_agenda_file', self.agenda, self.request)
        compormissos = view.get_compromissos()
        self.assertEqual(len(compormissos), 2)

    def test_get_compromissos_less(self):
        """Testa get_compromissos retornando o menor Compromisso."""
        self.request.set('initial_date', '2019-01-01')
        self.request.set('final_date', '2019-12-01')
        self.request.set('review_state', ['published'])
        view = api.content.get_view(
            'export_agenda_file', self.agenda, self.request)
        compormissos = view.get_compromissos()
        self.assertEqual(len(compormissos), 1)
        self.assertEqual(compormissos[0]['compromisso'], 'Compromisso 01')

    def test_get_compromissos_more(self):
        """Testa get_compromissos retornando o maior Compromisso."""
        self.request.set('initial_date', '2019-12-25')
        self.request.set('final_date', '2019-12-25')
        self.request.set('review_state', ['private'])
        view = api.content.get_view(
            'export_agenda_file', self.agenda, self.request)
        compormissos = view.get_compromissos()
        self.assertEqual(len(compormissos), 1)
        self.assertEqual(compormissos[0]['compromisso'], 'Compromisso 25')

    def test_write_csv(self):
        """Testa a geração do arquivo csv."""
        self.request.set('initial_date', '2019-01-01')
        self.request.set('final_date', '2019-12-25')
        self.request.set('review_state', ['private', 'published'])
        view = api.content.get_view(
            'export_agenda_file', self.agenda, self.request)
        csv = view.write_csv()
        linha0 = '"Título da Agenda","Descrição da Agenda","Nome do Órgão","Nome da Autoridade","Data da Agenda Diária","Informações Gerais","Compromisso","Local do Compromisso","Horário de Inicio","Horário de Término","Outros Participantes","Pauta"'
        linha1 = '"Agenda de Autoridade","Agenda de José","Órgão de José","José""01/12/2019","Atualização","Compromisso 01","Local""12:00","13:00","Maria","Pauta 01"'
        linha2 = '"Agenda de Autoridade","Agenda de José","Órgão de José","José""25/12/2019","Atualização","Compromisso 25","Local""08:00","09:00","Marta","Pauta 25"'
        self.assertIn(linha0, csv)
        self.assertIn(linha1, csv)
        self.assertIn(linha2, csv)

    def test_export_agenda_file(self):
        """Testa a view export_agenda_file."""
        self.request.set('initial_date', '2019-01-01')
        self.request.set('final_date', '2019-12-25')
        self.request.set('review_state', ['private', 'published'])
        view = api.content.get_view(
            'export_agenda_file', self.agenda, self.request)
        render_view = view()
        linha0 = '"Título da Agenda","Descrição da Agenda","Nome do Órgão","Nome da Autoridade","Data da Agenda Diária","Informações Gerais","Compromisso","Local do Compromisso","Horário de Inicio","Horário de Término","Outros Participantes","Pauta"'
        linha1 = '"Agenda de Autoridade","Agenda de José","Órgão de José","José""01/12/2019","Atualização","Compromisso 01","Local""12:00","13:00","Maria","Pauta 01"'
        linha2 = '"Agenda de Autoridade","Agenda de José","Órgão de José","José""25/12/2019","Atualização","Compromisso 25","Local""08:00","09:00","Marta","Pauta 25"'
        self.assertIn(linha0, render_view)
        self.assertIn(linha1, render_view)
        self.assertIn(linha2, render_view)
        headers = self.request.response.headers
        self.assertEqual(headers['content-type'], 'text/csv')
        self.assertEqual(
            headers['content-disposition'], 'attachment; filename="agenda.csv"')


class TestExportAgendaForm(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Site Administrator'])
        self.agenda = api.content.create(
            self.portal,
            'Agenda',
            'agenda',
            u'Agenda de Autoridade',
            autoridade=u'José',
        )
        self.view = api.content.get_view(
            'export_agenda', self.agenda, self.request)

    def test_fields_requires(self):
        """Testa os campos requeridos do form."""
        self.request.set('form.buttons.export', u'Export')
        html = self.view()
        self.assertIn('There were some errors', html)
        num_requires = html.count('Required input is missing.')
        self.assertEqual(num_requires, 3)

    def test_final_greater_initial(self):
        """Testa a validação da data final maior que a inicial."""
        self.request.set('form.widgets.initial_date-day', u'29')
        self.request.set('form.widgets.initial_date-month', u'12')
        self.request.set('form.widgets.initial_date-year', u'2020')
        self.request.set('form.widgets.final_date-day', u'01')
        self.request.set('form.widgets.final_date-month', u'12')
        self.request.set('form.widgets.final_date-year', u'2020')
        self.request.set('form.widgets.review_state', u'private')
        self.request.set('form.buttons.export', u'Export')
        html = self.view()
        self.assertIn('There were some errors', html)
        self.assertIn('Final date less than initial date', html)

    def test_final_greater_year(self):
        """Testa a validação da data final maior que 1 ano da inicial."""
        self.request.set('form.widgets.initial_date-day', u'01')
        self.request.set('form.widgets.initial_date-month', u'12')
        self.request.set('form.widgets.initial_date-year', u'2019')
        self.request.set('form.widgets.final_date-day', u'02')
        self.request.set('form.widgets.final_date-month', u'12')
        self.request.set('form.widgets.final_date-year', u'2020')
        self.request.set('form.widgets.review_state', u'private')
        self.request.set('form.buttons.export', u'Export')
        html = self.view()
        self.assertIn('There were some errors', html)
        self.assertIn('Final date greater than 1 year after the initial date', html)

    def test_form_export_redirect(self):
        """Testa o form redireciona para a view que gera o arquivo."""
        self.request.set('form.widgets.initial_date-day', u'29')
        self.request.set('form.widgets.initial_date-month', u'11')
        self.request.set('form.widgets.initial_date-year', u'2019')
        self.request.set('form.widgets.final_date-day', u'25')
        self.request.set('form.widgets.final_date-month', u'12')
        self.request.set('form.widgets.final_date-year', u'2019')
        self.request.set('form.widgets.review_state', u'private')
        self.request.set('form.buttons.export', u'Export')
        self.view()
        location = self.request.response.getHeader('location')
        self.assertEqual(
            'http://nohost/plone/agenda/export_agenda_file?'
            'initial_date=2019-11-29&final_date=2019-12-25'
            '&review_state=private',
            location,
        )
