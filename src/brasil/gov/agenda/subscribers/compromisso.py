# -*- coding: utf-8 -*-

from Acquisition import aq_base
from Acquisition import aq_parent
from brasil.gov.agenda.config import AGENDADIARIAFMT
from brasil.gov.agenda.config import PROJECTNAME
from brasil.gov.agenda.interfaces import IAgenda
from brasil.gov.agenda.interfaces import IAgendaDiaria
from brasil.gov.agenda.interfaces import ICompromisso
from five import grok
from OFS.event import ObjectWillBeMovedEvent
from Products.CMFPlone.utils import _createObjectByType
from zope.container.contained import notifyContainerModified
from zope.event import notify
from zope.lifecycleevent import ObjectMovedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

import datetime
import logging


logger = logging.getLogger(PROJECTNAME)


@grok.subscribe(IObjectAddedEvent)
@grok.subscribe(IObjectModifiedEvent)
def move_compromisso_para_agendadiaria(event, obj=None):
    """ Toda vez que um tipo compromisso for criado ou tiver sua
        data alterada
        ele sera movido para dentro de uma agenda diaria
    """
    if not obj:
        obj = event.object

    if not ICompromisso.providedBy(obj):  # nao eh um compromisso
        return

    start_date = getattr(obj, 'start_date', None)
    if not start_date:
        return

    formatted_date = start_date.strftime(AGENDADIARIAFMT)
    origin = aq_parent(obj)
    agenda = _get_agenda(origin)

    old_id = obj.getId()
    destination_id = formatted_date

    destination = _get_destination(agenda, obj, origin, destination_id)
    if not IAgendaDiaria.providedBy(destination):
        logger.warn('Objeto %s nao foi movido' % str(obj))
        # Reindexamos o SearchableText de origin
        origin.reindexObject(idxs=['SearchableText', ])
        return None

    new_id = _generate_id(destination, old_id)

    # Prepare to move object
    notify(ObjectWillBeMovedEvent(obj, origin, old_id, destination, new_id))
    obj.manage_changeOwnershipType(explicit=1)

    # Remove object from origin
    origin._delObject(old_id, suppress_events=True)
    obj = aq_base(obj)

    # Set new_id -- which is unique on destination
    obj._setId(new_id)

    # Persist object in destination
    destination._setObject(new_id, obj, set_owner=0, suppress_events=True)
    obj = destination._getOb(new_id)
    notify(ObjectMovedEvent(obj, origin, old_id, destination, new_id))
    notifyContainerModified(origin)
    notifyContainerModified(destination)
    obj._postCopy(destination, op=1)
    # try to make ownership implicit if possible
    obj.manage_changeOwnershipType(explicit=0)
    # Reindexamos o SearchableText de destination
    destination.reindexObject(idxs=['SearchableText', ])


def _get_agenda(base_folder):
    agenda = None
    while not IAgenda.providedBy(base_folder):
        base_folder = aq_parent(base_folder)
    agenda = base_folder
    return agenda


def _get_destination(agenda, obj, origin, destination_id):
    if destination_id not in agenda.objectIds():
        # Valores padrao para a AgendaDiaria
        autoridade = obj.autoridade
        location = obj.location
        # Criamos AgendaDiaria
        _createObjectByType('AgendaDiaria', agenda, id=destination_id)
        destination = agenda[destination_id]
        date = datetime.date(*[int(i) for i in destination_id.split('-')])
        destination.date = date
        destination.autoridade = autoridade
        destination.location = location
    else:
        destination = agenda[destination_id]
    destination_path = '/'.join(destination.getPhysicalPath())
    origin_path = '/'.join(origin.getPhysicalPath())
    is_children = origin_path.startswith(destination_path)
    allowed = _allowed_to_be_moved(obj, destination)
    if allowed and not is_children:
        return destination


def _generate_id(destination, old_id):
    taken = getattr(aq_base(destination), 'has_key', None)
    if taken is None:
        item_ids = set(destination.objectIds())
        taken = lambda x: x in item_ids
    if not taken(old_id):
        return old_id
    idx = 1
    while taken('%s.%d' % (old_id, idx)):
        idx += 1
    return '%s.%d' % (old_id, idx)


def _allowed_to_be_moved(obj, destination):
    err = ''
    try:
        obj._notifyOfCopyTo(destination, op=1)
    except Exception, e:
        err = str(e)
    if err:
        logger.warn(err)
        return False
    return True
