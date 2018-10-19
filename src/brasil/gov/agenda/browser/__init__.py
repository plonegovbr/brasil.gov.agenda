# -*- coding: utf-8 -*-
from brasil.gov.agenda.browser.agenda import AgendaJSONView  # noqa: F401
from brasil.gov.agenda.browser.agenda import AgendaView  # noqa: F401
from brasil.gov.agenda.browser.agendadiaria import AgendaDiariaView  # noqa: E501,F401
from brasil.gov.agenda.browser.compromisso import CompromissoView  # noqa: E501,F401
from brasil.gov.agenda.browser.ics import ICSView  # noqa: F401
from brasil.gov.agenda.browser.vcs import VCSView  # noqa: F401
from plone.app.layout.viewlets import ViewletBase


class ResourcesViewlet(ViewletBase):
    """This viewlet inserts static resources on page header."""
