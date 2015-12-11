# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='spam',
    version='0.3.1',
    description='A project and asset manager for 3d animation and VFX productions',
    author='Lorenzo Pierfederici',
    author_email='lpierfederici@gmail.com',
    #url='',
    license='GPL v3',
    zip_safe=False,
    install_requires=[
        # "TurboGears2 == 2.1.5",
        "TurboGears2 == 2.2.0",
        # "TurboGears2 == 2.2.1",
        # "Pylons==0.9.7",
        "Pylons==1.0",
        "WebTest==1.4.3",
        "Babel",
        "tw2.core==2.0b4",
        "tw2.forms==2.0b4",
        "tw2.dynforms==2.0a1",
        "zope.sqlalchemy",
        "repoze.tm2",
        "repoze.what-quickstart",
        "repoze.what-pylons==1.0",
        "mercurial == 1.9",
        # if we dont use mysql as database backend we can omit this package
        # to avoid cluttering of our sistem with unided stuff
        #"MySQL-python",
        # "sqlalchemy-migrate == 0.5.4",
        "sqlalchemy-migrate",
        "PasteScript",
        # "WebOb==1.0.8",
        "WebOb==1.1.1",
        "PasteDeploy",
        "decorator",
        "WebError",
        "simplejson",
        "Pygments",
        "nose",
        # "SQLAlchemy == 0.6.3",
        "SQLAlchemy == 0.9.10",
        # "SQLAlchemy",
        "Mako",
        "WebHelpers",
                ],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'spam'],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['WebTest', 'BeautifulSoup'],
    package_data={'spam': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    message_extractors={'spam': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('public/**', 'ignore', None)]},

    entry_points="""
    [paste.app_factory]
    main = spam.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [paste.paster_command]
    build-docs = spam.commands.docs:BuildDocs
    build-client = spam.commands.client:BuildClient
    """,
)
