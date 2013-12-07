mercy
=====

This project comprises the entirety of The Mercy Project; everything needed to deploy and serve The Mercy Project currently lives in this repository.

If you came here looking for more information about what (in general) The Mercy Project is, please see http://www.mercyproject.us for more information

Python Application
===================

The mercy/ directory contains all of the python code used to serve the Mercy website and perform all necessary functions.

Alembic ORM database upgrade scripts
====================================

The alembic/ directory contains scripts used by the alembic flask extension to automatically upgrade and downgrade the postgres database used by Mercy.

Puppet Modules for Deployment
==============================

The puppet code necessary to deploy Mercy onto Linux servers lives in the puppet/ directory.

Nagios Checks for Monitoring the Mercy Platform
===============================================

These live in the nagios/ directory.

Automated Test Suites
=====================

tests/ currently holds any and all automated testing (Python Nosetests, currently) for all of the code listed above.
