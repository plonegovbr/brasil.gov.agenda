# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0a3'
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
        'Development Status :: 3 - Alpha',
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
        'collective.portlet.calendar',
        'plone.app.content',
        'plone.app.contenttypes',
        'plone.app.dexterity [grok]',
        'plone.app.portlets',
        'plone.app.referenceablebehavior',
        'plone.app.upgrade',
        'plone.app.upgrade',
        'plone.app.versioningbehavior',
        'plone.app.vocabularies',
        'plone.behavior',
        'plone.dexterity',
        'plone.directives.form',
        'plone.portlets',
        'plone.supermodel >=1.2.3',
        'plone.uuid',
        'Products.CMFCore',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.component',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
        ],
    },
    entry_points='''
      [z3c.autoinclude.plugin]
      target = plone
      ''',
)
