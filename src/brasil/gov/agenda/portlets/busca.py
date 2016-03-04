# -*- coding: utf-8 -*-

from brasil.gov.agenda import _
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implementer


class IBuscaPortlet(IPortletDataProvider):
    """ Portlet de busca dentro da agenda
    """

    root = schema.Choice(
        title=_(u'Raiz'),
        description=_(u'Informe a raiz da busca de Agendas Diarias'),
        required=False,
        source=SearchableTextSourceBinder({'is_folderish': True},
                                          default_query='path:'))


@implementer(IBuscaPortlet)
class Assignment(base.Assignment):

    root = None

    def __init__(self, root=None):
        self.root = root

    @property
    def title(self):
        return _(u'Busca de Agenda')


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('busca.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        portal_state = getMultiAdapter((context, request),
                                       name='plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()

    def root(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        if self.data.root:
            navigation_root_path = '%s%s' % (portal_state.navigation_root_path(),  # NOQA
                                             self.data.root)
        else:
            navigation_root_path = portal_state.navigation_root_path()
        return navigation_root_path

    def portal_types(self):
        return ['AgendaDiaria', ]

    def search_action(self):
        return '%s/@@search' % self.navigation_root_url


class AddForm(base.AddForm):
    form_fields = form.Fields(IBuscaPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u'Adiciona Portlet de Busca de Agenda')
    description = _(u'Este portlet busca no conteudo de agendas diarias.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IBuscaPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u'Adiciona Portlet de Busca de Agenda')
    description = _(u'Este portlet busca no conteudo de agendas diarias.')
