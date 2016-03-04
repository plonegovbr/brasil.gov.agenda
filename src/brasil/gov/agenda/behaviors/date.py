# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import AGENDADIARIAFMT
from plone.app.content.interfaces import INameFromTitle
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import datetime


class INameFromDate(Interface):
    """Marker interface to enable name from date behavior"""


@adapter(INameFromDate)
@implementer(INameFromTitle)
class NameFromDate(object):

    def __new__(cls, context):
        date = getattr(context, 'date', None)
        if not isinstance(date, datetime.date):
            return None
        formated_date = date.strftime(AGENDADIARIAFMT)
        instance = super(NameFromDate, cls).__new__(cls)
        instance.title = formated_date
        if safe_hasattr(context, 'title') and not context.title:
            context.title = formated_date
        return instance

    def __init__(self, context):
        pass
