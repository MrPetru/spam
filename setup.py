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
        "TurboGears2 >= 2.1b2",
        "Babel >=0.9.4",
        "tw2.core",
        "tw2.forms",
        "tw2.dynforms",
        "zope.sqlalchemy",
        "repoze.tm2 >= 1.0a4",
        "repoze.what-quickstart >= 1.0",
        "mercurial == 1.6.3",
        # if we dont use mysql as database backend we can omit this package
        # to avoid cluttering of our sistem with unided stuff
        #"MySQL-python",
        "sqlalchemy-migrate == 0.5.4",
        "PasteScript >= 1.7",
        "WebOb == 0.9.8",
        "PasteDeploy == 1.3.3",
        "decorator == 3.2.0",
        "WebError == 0.10.1",
        "simplejson == 2.1.1",
        "Pygments == 1.1.1",
        "nose == 0.11.1",
        "SQLAlchemy == 0.6.3",
        "Mako == 0.3.4",
        "WebHelpers == 1.3",
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
