# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import TZ
from brasil.gov.agenda.interfaces import IAgendaDiaria
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from DateTime import DateTime
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile.file import NamedBlobImage
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import datetime
import os
import unittest


TEST_JPEG_FILE = open(
    os.path.sep.join(__file__.split(os.path.sep)[:-1] + ['brasil.jpg', ]),
    'rb'
).read()


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.ct = self.portal.portal_catalog
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        # Criamos a agenda
        self.folder.invokeFactory('Agenda', 'agenda')
        self.agenda = self.folder['agenda']
        self.agenda.image = NamedBlobImage(data=TEST_JPEG_FILE,
                                           filename=u'brasil.jpg')
        # Criamos a agenda diaria
        self.agenda.invokeFactory('AgendaDiaria', '2013-02-05')
        self.agendadiaria = self.agenda['2013-02-05']
        self.agendadiaria.autoridade = u'Clarice Lispector'
        self.agendadiaria.date = datetime.datetime(2013, 2, 5)
        self.agendadiaria.reindexObject()

    def test_adding(self):
        self.assertTrue(IAgendaDiaria.providedBy(self.agendadiaria))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='AgendaDiaria')
        self.assertIsNotNone(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='AgendaDiaria')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IAgendaDiaria.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.agendadiaria))
        self.assertTrue(IAttributeUUID.providedBy(self.agendadiaria))

    def test_exclude_from_nav(self):
        results = self.ct.searchResults(portal_type='AgendaDiaria')
        brain = results[0]
        self.assertTrue(brain.exclude_from_nav)

    def test_exclude_from_nav_behavior(self):
        self.assertFalse(IExcludeFromNavigation.providedBy(self.agendadiaria))

    def test_subjects_catalog(self):
        agendadiaria = self.agendadiaria
        agendadiaria.subjects = (u'Brasil', u'México')
        agendadiaria.reindexObject(idxs=['Subject'])
        ct = self.portal.portal_catalog
        results = ct.searchResults(portal_type='AgendaDiaria')
        b = results[0]
        self.assertIn('Brasil', b.Subject)
        self.assertIn('México', b.Subject)

    def test_default_subjects(self):
        from brasil.gov.agenda.content.agendadiaria import default_subjects
        agenda = self.agenda
        agenda.subjects = (u'Brasil', u'México')
        # default_factory é executado no container
        self.assertIn(u'Brasil', default_subjects(agenda))
        self.assertIn(u'México', default_subjects(agenda))

    def test_datevalidator(self):
        from brasil.gov.agenda.content.agendadiaria import DateValidator
        from zope.interface.exceptions import Invalid
        import zope

        class IAgendaDiaria(zope.interface.Interface):
            date = zope.schema.Date(title=u'Date', required=True)

        validator = DateValidator(None, None, None,
                                  IAgendaDiaria['date'], None)
        validator.context = self.agenda
        # Se usarmos a data de uma agendadiaria existente
        # teremos um erro
        self.assertRaises(Invalid,
                          validator.validate,
                          datetime.date(2013, 2, 5))
        # Se usarmos outra data o validador retornara None
        self.assertEqual(None,
                         validator.validate(datetime.date(2013, 2, 6)))

    def test_title(self):
        agendadiaria = self.agendadiaria
        self.assertEqual(agendadiaria.Title(),
                         'Agenda de Clarice Lispector para 05/02/2013')

    def test_effective_date_indexing(self):
        ct = self.ct
        with api.env.adopt_roles(['Manager']):
            # Conteudo publicado
            api.content.transition(
                self.agendadiaria,
                'publish'
            )
            # Data no passado
            self.agendadiaria.date = datetime.datetime(2013, 2, 5)
            self.agendadiaria.reindexObject()
        # Como usuario anonimo, podemos ver o conteudo
        with api.env.adopt_roles(['Anonymous']):
            results = ct.searchResults(portal_type='AgendaDiaria')
            self.assertEqual(len(results), 1)
            self.assertTrue(
                results[0].EffectiveDate.startswith('2013-02')
            )
        # Manager
        with api.env.adopt_roles(['Manager']):
            self.agendadiaria.date = datetime.datetime(2029, 10, 17)
            self.agendadiaria.reindexObject()
        # Anonimo Publico
        with api.env.adopt_roles(['Anonymous']):
            # Para um conteudo no futuro, tambem devemos ver o conteudo
            results = ct.searchResults(portal_type='AgendaDiaria')
            self.assertEqual(len(results), 1)
            self.assertTrue(
                results[0].EffectiveDate.startswith('2029-10')
            )
        # Manager
        with api.env.adopt_roles(['Manager']):
            api.content.transition(
                self.agendadiaria,
                'reject'
            )
        # Anonimo Privado
        with api.env.adopt_roles(['Anonymous']):
            # Para um conteudo no futuro, tambem devemos ver o conteudo
            results = ct.searchResults(portal_type='AgendaDiaria')
            self.assertEqual(len(results), 1)
            today = datetime.date.today().strftime('%Y-%m')
            self.assertTrue(
                results[0].EffectiveDate.startswith(today)
            )

    def test_start_indexing(self):
        ct = self.ct
        self.agendadiaria.date = datetime.datetime(2013, 2, 5)
        self.agendadiaria.reindexObject()
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   start={'query': DateTime('2013-02-06'),
                                          'range': 'max'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].start.timezone(), TZ)
        self.agendadiaria.date = datetime.datetime(2013, 10, 17)
        self.agendadiaria.reindexObject()
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   start={'query': DateTime('2013-10-17'),
                                          'range': 'min'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].start.timezone(), TZ)

    def test_end_indexing(self):
        ct = self.ct
        self.agendadiaria.date = datetime.datetime(2013, 2, 6)
        self.agendadiaria.reindexObject()
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   end={'query': DateTime('2013-02-06'),
                                        'range': 'min'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].end.timezone(), TZ)
        self.agendadiaria.date = datetime.datetime(2013, 10, 17)
        self.agendadiaria.reindexObject()
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   end={'query': DateTime('2013-10-17'),
                                        'range': 'min'})
        self.assertEqual(results[0].end.timezone(), TZ)

    def test_SearchableText_indexing_sem_compromissos(self):
        ct = self.ct
        self.agendadiaria.location = u'Esplanada dos Ministerios'
        self.agendadiaria.autoridade = u'Clarice Lispector'
        self.agendadiaria.reindexObject()
        # Busca pela autoridade deve retornar resultados
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='Clarice')
        self.assertEqual(len(results), 1)
        # Busca pelo local deve retornar resultados
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='Esplanada')
        self.assertEqual(len(results), 1)

        # Ao alterar o local e autoridade devemos ficar sem resultados
        self.agendadiaria.location = u'Palacio do Planalto'
        self.agendadiaria.autoridade = u'Juscelino Kubitschek'
        self.agendadiaria.update = RichTextValue(u'Alterado local e autoridade',
                                                 'text/html',
                                                 'text/x-html-safe',
                                                 encoding='utf-8')
        self.agendadiaria.reindexObject()
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='Clarice')
        self.assertEqual(len(results), 0)
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='Esplanada')
        self.assertEqual(len(results), 0)
        # Porem busca por Alterado deve retornar algo
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='Alterado')
        self.assertEqual(len(results), 1)

    def test_SearchableText_indexing_com_compromissos(self):
        ct = self.ct
        agendadiaria = self.agendadiaria
        start_date = datetime.datetime(2013, 2, 5, 10, 0, 0)
        agendadiaria.invokeFactory('Compromisso', 'reuniao-ministerial',
                                   start_date=start_date)
        reuniao = agendadiaria['reuniao-ministerial']
        reuniao.title = u'Reunião Ministerial'
        reuniao.description = u'Encontro com todos os ministros'
        reuniao.autoridade = u'Clarice Lispector'
        reuniao.location = u'Palacio do Planalto'
        reuniao.attendees = u'Mario de Andrade\nTarsila do Amaral'
        reuniao.reindexObject()
        # Informamos que o objeto foi modificado
        # Isto deve reindexar a AgendaDiaria
        notify(ObjectModifiedEvent(reuniao))
        # Realizamos a busca informando um dos participantes
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='Tarsila')
        self.assertEqual(len(results), 1)

        # Realizamos a busca informando parte da pauta
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='ministros')
        self.assertEqual(len(results), 1)

        # Realizamos a busca informando titulo
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='Ministerial')
        self.assertEqual(len(results), 1)

        # Realizamos a busca informando local
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='Planalto')
        self.assertEqual(len(results), 1)

        # Realizamos a busca informando autoridade
        results = ct.searchResults(portal_type='AgendaDiaria',
                                   SearchableText='Clarice')
        self.assertEqual(len(results), 1)

    def test_view_sem_compromissos(self):
        agendadiaria = self.agendadiaria
        view = agendadiaria.restrictedTraverse('@@view')
        # AgendaDiaria sem compromissos e sem nada no campo atualizacao
        view.update()
        sem_compromissos = view.exibe_sem_compromissos()
        self.assertTrue(sem_compromissos)

        # Adicionamos uma informacao no campo atualizacao
        agendadiaria.update = RichTextValue(u'Alterado local e autoridade',
                                            'text/html',
                                            'text/x-html-safe',
                                            encoding='utf-8')
        view.update()
        sem_compromissos = view.exibe_sem_compromissos()
        self.assertFalse(sem_compromissos)

        # Removemos a atualizacao e adicionamos um compromisso
        agendadiaria.update = None
        start_date = datetime.datetime(2013, 2, 5, 10, 0, 0)
        agendadiaria.invokeFactory('Compromisso', 'reuniao-ministerial',
                                   start_date=start_date)
        reuniao = agendadiaria['reuniao-ministerial']
        reuniao.title = u'Reunião Ministerial'
        reuniao.description = u'Encontro com todos os ministros'
        reuniao.autoridade = u'Clarice Lispector'
        reuniao.location = u'Palacio do Planalto'
        reuniao.attendees = u'Mario de Andrade\nTarsila do Amaral'
        reuniao.reindexObject()
        view.update()
        sem_compromissos = view.exibe_sem_compromissos()
        self.assertFalse(sem_compromissos)

    def test_agendadiaria_icon(self):
        from plone.testing.z2 import Browser
        portal = self.portal
        app = self.layer['app']

        browser = Browser(app)
        portal_url = portal.absolute_url()

        browser.open('%s/++resource++brasil.gov.agenda/agenda_icon.png' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')

    def test_agendadiaria_view_imagem(self):
        view = self.agendadiaria.restrictedTraverse('@@view')
        view.update()
        self.assertIn(u'<img src="http://nohost/plone/test-folder/agenda/@@images/',
                      view.imagem())

    def test_agendadiaria_persiste_data(self):
        from brasil.gov.agenda import utils

        # Realizamos o monkey patch da funcao tomorrow, usada pelo
        # agendadiaria.default_date assim ele retornara a data de 25/12/2013
        def mocked_tomorrow():
            return datetime.date(2013, 12, 25)

        utils._tomorrow = utils.tomorrow
        utils.tomorrow = mocked_tomorrow

        # Criamos uma agenda para o dia seguibte.
        self.agenda.invokeFactory('AgendaDiaria', '2013-12-25')
        obj = self.agenda['2013-12-25']
        obj.autoridade = u'Clarice Lispector'
        self.assertEqual(obj.date, datetime.date(2013, 12, 25))

        # Agora retornamos dia 31/12/2013 na funcao tomorrow
        # o valor do campo date do objeto nao deve se alterar
        def mocked_tomorrow():
            return datetime.date(2013, 12, 30)

        setattr(utils, 'tomorrow', mocked_tomorrow)

        self.assertEqual(obj.date, datetime.date(2013, 12, 25))

        # Voltamos o metodo ao seu valor original
        setattr(utils, 'tomorrow', utils._tomorrow)
