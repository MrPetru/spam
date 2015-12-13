The *Spark Project & Asset Manager* is a web application originally developed at
`Spark Digital Entertainment <http://www.sparkde.com>`_ to help manage the
production workflow of a 3d animation or VFX pipeline


Installation and Setup of a development environment for SPAM
============================================================

Create a directory where to install SPAM::

    $ mkdir ~/spam


Move to the newly created directory::

    $ cd ~/spam


Create a virtual environment::

    $ virtualenv --python=python2.7 spamenv


Activate the virtual environment::

    $ source spamenv/bin/activate


Clone SPAM repository::

    $ git clone http://github.com/MrPetru/spam.git source


Move to the newly created spam source directory::

    $ cd source


Switch to branch home_with_tasks::

    $ git checkout home_with_tasks


Install all requirements, create egginfo and install in the virtualenv in
*develop* mode::

    $ python setup.py develop

**Note: there will be an error related to mercurial. use this command to installa mercurial manually**::

    $ pip install https://www.mercurial-scm.org/release/mercurial-1.9.3.tar.gz


Edit the configuration file ``development.ini`` for your environment::
Note: it's better to create a local copy and use that for installation.

    $ cp -v development.ini development_local.ini


Setup the application (this setup a database and creates data directories)::

    $ paster setup-app --name=SPAM development_local.ini


Allow the virtualenv to access locally installed packages (needed for gstreamer-python)::

    $ rm ../spamenv/lib/python2.7/no-global-site-packages.txt


Serve SPAM through a paste server::

    $ paster serve --reload development_local.ini


Access spam from a web-browser ro the address you inserted in development_local.ini file::

    http://localhost:8080


Log-in as::

    User name:  admin
    Password:   none


Enjoy :)
