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


# iCal header and footer
ICS_HEADER = """\
BEGIN:VCALENDAR
PRODID:%(prodid)s
VERSION:2.0
METHOD:PUBLISH
"""

ICS_FOOTER = """\
END:VCALENDAR
"""

# iCal event
ICS_EVENT_START = """\
BEGIN:VEVENT
DTSTAMP:%(dtstamp)s
CREATED:%(created)s
UID:ATEvent-%(uid)s
LAST-MODIFIED:%(modified)s
SUMMARY:%(summary)s
DTSTART:%(startdate)s
DTEND:%(enddate)s
"""

ICS_EVENT_END = """\
CLASS:PUBLIC
END:VEVENT
"""


class ICSView (grok.View):
    """ Visao vCal
    """
    grok.name('ical_view')
    grok.context(ICompromisso)

    def getICal(self):
        """get iCal data
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
        out.write(ICS_EVENT_START % map)

        description = context.Description()
        if description:
            out.write(foldLine('DESCRIPTION:%s\n' % vformat(description)))

        location = context.location
        if location:
            location = location.encode('utf-8')
            out.write('LOCATION:%s\n' % vformat(location))

        cn = []
        contact = context.autoridade
        if contact:
            cn.append(contact)
        if cn:
            out.write('CONTACT:%s\n' % vformat(', '.join(cn)))

        url = context.absolute_url()
        if url:
            out.write('URL:%s\n' % url)

        out.write(ICS_EVENT_END)
        return out.getvalue()

    def render(self):
        """vCalendar output
        """
        response = self.request.response
        response.setHeader('Content-Type', 'text/calendar')
        response.setHeader('Content-Disposition',
                           'attachment; filename="%s.ics"' % self.context.getId())
        out = StringIO()
        out.write(ICS_HEADER % {'prodid': PROJECTNAME})
        out.write(self.getICal())
        out.write(ICS_FOOTER)
        return n2rn(out.getvalue())
