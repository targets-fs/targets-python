===============================
Targets Python
===============================

.. image:: https://img.shields.io/pypi/v/targets.svg
        :target: https://pypi.python.org/pypi/targets

.. image:: https://img.shields.io/travis/targets-fs/targets-python.svg
        :target: https://travis-ci.org/targets-fs/targets-python

.. image:: https://readthedocs.org/projects/targets/badge/?version=latest
        :target: https://readthedocs.org/projects/targets/?badge=latest
        :alt: Documentation Status


Targets is the simplified universal file system

* Free software: ISC license
* Documentation: https://targets.readthedocs.org.


Description
-----------
Most of the initial code is contributed by luigi project
Started as discussion: https://groups.google.com/forum/#!topic/luigi-user/ZLGJCj0dBJI

...
As a Luigi user for the past couple of years, I have found out that I am using the concept of Luigi targets in most of the projects I was working on. Transparent file system, atomic write/reads, formats is a great functionality, and is highly missing from the global Python eco system. Moreover, going over multiple workflow management project implementations(mrjob,airflow) I have always been surprised to see yet another implementation of the abstraction over fs/ssh/s3/ftp/etc all over again.

As a developer, and especially as a Python developer, I want to focus on implementation of my business requirements, instead of working with low level filesystem APIs. The standard "open" function is simply not strong enough.
...


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_  `evgenyshulman/cookiecutter-pypackage`_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`evgenyshulman/cookiecutter-pypackage`: https://github.com/evgenyshulman/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Initial version of Targets is based on Luigi_ project.

.. _Luigi: https://github.com/spotify/luigi


Luigi was built at `Spotify <https://www.spotify.com/us/>`_, mainly by
`Erik Bernhardsson <https://github.com/erikbern>`_ and
`Elias Freider <https://github.com/freider>`_.
`Many other people <https://github.com/spotify/luigi/graphs/contributors>`_
have contributed since open sourcing in late 2012.
`Arash Rouhani <https://github.com/tarrasch>`_ is currently the chief
maintainer of Luigi.


