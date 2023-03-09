========
RstCloth
========

Background and Goals
--------------------

reStructuredText is a powerful human-centric markup language that is
well defined, flexible, with powerful tools that make writing and
maintaining text easy and pleasurable. Humans can edit
reStructuredText without the aide of complex editing tools, and the
resulting source is easy to manipulate and process.

One of the key features of reStructuredText is it's relatively
complete extension API, which makes it possible to minimize fragile
repetitive structures in source files and increase the ease of
production. While you can use these extensions to build
custom content types with ease, extensions make reStructuredText source less
portable and less intuitive to edit for casual contributors.

As an alternative and a supplement, RstCloth is a Python API for
writing well formed reStructuredText programatically. RstCloth
facilitates :

- generating data-driven content views into existing reStructuredText
  environments and tools.

- automating content generation and modification without creating
  unportable-restructured text.

- ensuring that the tool chain is easily debugable by using
  transparent intermediate formats.

Status
------

RstCloth is undergoing ongoing development and expansion is not
stable at this point. Current features and projects include:

- improve documentation.

- develop unit testing framework to ensure consistent API behavior.

- build/extend a table generation API.

- Add a chart generation API for ``sphinx-charts``.

- improve paragraph level content generation API.


.. _contents:

Contents
========

.. toctree::
   :maxdepth: 2

   self
   installation
   quick_start
   rstcloth
   license
   version_history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
