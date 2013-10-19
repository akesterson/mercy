mercy
=====

A puppet module for installing the Mercy Flask application

Requirements
============

This puppet module assumes that you have:

* A RabbitMQ broker that we can use for Celery tasks
* Working apache on localhost with a puppet service we can notify
* Working python 2.7 and pip on localhost
* Working postgres with a username, password, and database for mercy to use

Aside from that, the module has no dependencies.

Usage
=========

    class { 'mercy':
        # ---- These are required, they have no defaults
        environment    => 'dev|production',
        version        => 'absent|latest|MAJOR-MINOR',
        ensure         => 'running|stopped'.
        rabbitmq_uri   => 'RABBITMQ_BROKER_URI',
        # ---- Everything below is optional
	rabbitmq_user  => 'mercy',
	rabbitmq_pw    => 'mercy',
	rabbitmq_vhost => 'mercy',
        vhost_dir      => '/etc/apache/httpd/conf.d',
        apache_service => 'httpd',
        postgres_uri   => 'localhost',
        postgres_user  => 'mercy',
        postgres_pw    => 'mercy',
        postgres_db    => 'mercy'
    }

If 'environment' is dev, then the mercy application will be installed via a tarball located in ./mercy/files/mercy-${ensure}.tar.gz. If 'environment' is production, then mercy will be installed via pip and ensured at the given version.

Events
======

This puppet module will notify your apache service whenever the vhost is modified, or the mercy application version is updated, since an apache graceful restart will be required in either case.
