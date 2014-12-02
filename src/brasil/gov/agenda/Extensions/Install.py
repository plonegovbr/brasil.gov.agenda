# -*- coding: utf-8 -*-
from plone import api


def uninstall(portal, reinstall=False):
    if not reinstall:
        tinymce = api.portal.get_tool('portal_tinymce')
        linkable = tinymce.linkable.split()
        if 'Agenda' in linkable:
            linkable.remove('Agenda')
            tinymce.linkable = u'\n'.join(linkable)
            return 'Agenda removed from linkable types in TinyMCE.'
