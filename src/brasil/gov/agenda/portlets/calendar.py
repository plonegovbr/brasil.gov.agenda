# -*- coding: utf-8 -*-

from brasil.gov.agenda.interfaces import IAgenda
from collective.portlet.calendar import calendar
from plone.memoize.compress import xhtml_compress
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Renderer(calendar.Renderer):

    _agenda_template = ViewPageTemplateFile('calendar.pt')

    def update(self):
        super(Renderer, self).update()
        yearmonth = self.yearmonth
        # HACK: Exibiremos os 10 ultimos anos.
        # Precisamos de algo que controle o numero de anos a serem
        # exibidos. Este eh um problema do Plone
        self.showPrevMonth = yearmonth > (self.now[0] - 10, self.now[1])

    def render(self):
        if self.is_agenda():
            return xhtml_compress(self._agenda_template())
        else:
            return xhtml_compress(self._template())

    def is_agenda(self):
        root_path = self.root()
        root = self.context.restrictedTraverse(root_path)
        return IAgenda.providedBy(root)

    def root_url(self):
        root_path = self.root()
        root = self.context.restrictedTraverse(root_path)
        return root.absolute_url()

    def getEventsForCalendar(self):
        weeks = super(Renderer, self).getEventsForCalendar()
        for week in weeks:
            for day in week:
                if not day.get('date_string'):
                    continue
                date_ = day['date_string'].split('-')
                date_ = [int(p) for p in date_]
                day['date_string'] = '%04d-%02d-%02d' % (date_[0], date_[1], date_[2],)
        return weeks

    def get_agendasdiarias(self):
        root_path = self.root()
        root = self.context.restrictedTraverse(root_path)
        year = self.year
        month = self.month
        objIds = root.objectIds()
        prefix = '%s-%s' % (str(year), str(month))
        agendasdiarias = [oId for oId in objIds if oId.startswith(prefix)]
        agendasdiarias.sort()
        agendasdiarias.reverse()
        return agendasdiarias
