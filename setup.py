from distutils.core import setup
import mercy.version
import os
import sys

if __name__ == "__main__":
    setup(
        name="mercy",
        url="https://www.github.com/akesterson/mercy",
        version=mercy.version.VERSION,
        description="A web application that facilitates charitable prescription payments",
        long_description="",
        author=("Andrew Kesterson"),
        author_email="andrew@aklabs.net",
        license="MIT",
        install_requires=["flask",
                          "sqlalchemy",
                          "alembic",
                          "psycopg2",
                          "flask-sqlalchemy"],
        scripts=["scripts/mercy.wsgi"],
        packages=["mercy",
                  "mercy/models",
                  "mercy/importers"],
        data_files=[],
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Web Environment',
            'Framework :: Flask',
            'Intended Audience :: Healthcare Industry',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 2.7',
            'Topic :: Other/Nonlisted Topic',
        ],
    )

