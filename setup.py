# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '2.0b2'
description = 'Agenda de membros do Governo Brasileiro'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='brasil.gov.agenda',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plonegovbr agenda brasil plone dexterity',
    author='PloneGovBr',
    author_email='gov@plone.org.br',
    url='https://github.com/plonegovbr/brasil.gov.agenda',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['brasil', 'brasil.gov'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Acquisition',
        'collective.portlet.calendar',  # BBB: https://github.com/plonegovbr/brasil.gov.agenda/issues/137
        'collective.cover',
        'plone.api',
        'plone.app.content',
        'plone.app.contentlisting',
        'plone.app.contenttypes',
        'plone.app.dexterity',
        'plone.app.form',
        'plone.app.imaging',
        'plone.app.portlets',
        'plone.app.referenceablebehavior',
        'plone.app.uuid',
        'plone.app.versioningbehavior',
        'plone.autoform',
        'plone.batching',
        'plone.behavior',
        'plone.dexterity',
        'plone.indexer',
        'plone.namedfile',
        'plone.portlets',
        'plone.supermodel',
        'plone.tiles',
        'plone.uuid',
        'Products.ATContentTypes',
        'Products.CMFPlone >= 4.3',
        'Products.GenericSetup',
        'setuptools',
        'six',
        'zope.component',
        'zope.container',
        'zope.event',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.publisher',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.app.textfield',
            'plone.browserlayer',
            'plone.namedfile',
            'plone.testing',
            'robotsuite',
            'transaction',
            'zope.site',
        ],
    },
    entry_points='''
      [z3c.autoinclude.plugin]
      target = plone
      ''',
)
