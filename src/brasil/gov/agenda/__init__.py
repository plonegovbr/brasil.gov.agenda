# -*- coding: utf-8 -*-

from brasil.gov.agenda import patches
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('brasil.gov.agenda')


patches.run()
