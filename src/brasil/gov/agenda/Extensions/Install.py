# -*- coding: utf-8 -*-
from plone import api


def uninstall(portal, reinstall=False):
    if not reinstall:
        tinymce = api.portal.get_tool('portal_tinymce')
        linkable = tinymce.linkable.split()
        for t in ('Agenda', 'AgendaDiaria', 'Compromisso'):
            if t in linkable:
                linkable.remove(t)
        tinymce.linkable = u'\n'.join(linkable)
        return 'Package content types are no longer linkable on TinyMCE.'
