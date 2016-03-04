# -*- coding: utf-8 -*-

from brasil.gov.agenda.config import PROJECTNAME
from brasil.gov.agenda.interfaces import ICompromisso
from brasil.gov.agenda.utils import rfc2445dt
from cStringIO import StringIO
from DateTime import DateTime
from five import grok
from plone.uuid.interfaces import IUUID
from Products.ATContentTypes.lib.calendarsupport import foldLine
from Products.ATContentTypes.lib.calendarsupport import n2rn
from Products.ATContentTypes.lib.calendarsupport import vformat


# vCal header and footer
VCS_HEADER = """\
BEGIN:VCALENDAR
PRODID:%(prodid)s
VERSION:1.0
"""

VCS_FOOTER = """\
END:VCALENDAR
"""

# vCal event
VCS_EVENT_START = """\
BEGIN:VEVENT
DTSTART:%(startdate)s
DTEND:%(enddate)s
DCREATED:%(created)s
UID:Compromisso-%(uid)s
SEQUENCE:0
LAST-MODIFIED:%(modified)s
SUMMARY:%(summary)s
"""

VCS_EVENT_END = """\
PRIORITY:3
TRANSP:0
END:VEVENT
"""


class VCSView (grok.View):
    """ Visao vCal
    """
    grok.name('vcal_view')
    grok.context(ICompromisso)

    def getVCal(self):
        """get vCal data
        """
        context = self.context
        out = StringIO()
        map = {
            'dtstamp': rfc2445dt(DateTime()),
            'created': rfc2445dt(DateTime(context.CreationDate())),
            'uid': IUUID(context),
            'modified': rfc2445dt(DateTime(context.ModificationDate())),
            'summary': vformat(context.Title()),
            'startdate': rfc2445dt(context.start_date),
            'enddate': rfc2445dt(context.end_date),
        }
        out.write(VCS_EVENT_START % map)
        description = context.Description()
        if description:
            out.write(foldLine('DESCRIPTION:%s\n' % vformat(description)))
        location = context.location
        if location:
            location = location.encode('utf-8')
            out.write('LOCATION:%s\n' % vformat(location))
        out.write(VCS_EVENT_END)
        return out.getvalue()

    def render(self):
        """vCalendar output
        """
        response = self.request.response
        response.setHeader('Content-Type', 'text/x-vCalendar')
        response.setHeader('Content-Disposition',
                           'attachment; filename="%s.vcs"' % self.context.getId())
        out = StringIO()
        out.write(VCS_HEADER % {'prodid': PROJECTNAME})
        out.write(self.getVCal())
        out.write(VCS_FOOTER)
        return n2rn(out.getvalue())
