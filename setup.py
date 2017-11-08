# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.1.1'
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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
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
        'collective.cover',
        'collective.portlet.calendar',
        'plone.api',
        'plone.app.content',
        'plone.app.contenttypes',
        'plone.app.dexterity [grok]',
        'plone.app.portlets',
        'plone.app.referenceablebehavior',
        'plone.app.textfield',
        'plone.app.upgrade',
        'plone.app.uuid',
        'plone.app.versioningbehavior',
        'plone.app.vocabularies',
        'plone.behavior',
        'plone.dexterity',
        'plone.directives.form',
        'plone.indexer',
        'plone.memoize',
        'plone.portlets',
        'plone.supermodel',
        'plone.uuid',
        'Products.ATContentTypes',
        'Products.CMFCore',
        'Products.CMFPlone >= 4.3',
        'Products.CMFQuickInstallerTool',
        'Products.GenericSetup',
        'setuptools',
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
