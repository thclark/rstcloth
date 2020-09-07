.. rstcloth documentation master file, created by
   sphinx-quickstart on Thu Oct 20 20:31:16 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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

One of the key features of reSturcturedText is it's relatively
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

Example Use
-----------

The following RstCloth code: ::

   from rstcloth import RstCloth

   d = RstCloth()


   d.title('Example Use')
   d.newline()
   d.h2('Contents')
   d.directive(name="contents", fields=[('local', ''), ('backlinks', 'None')])
   d.newline()
   d.h2('Code -- shebang')
   d.codeblock('#!/usr/bin/env')

   d.print_content()

Would result in the following reStructuredText: ::

   ===========
   Example Use
   ===========

   Contents
   --------

   .. contents::
      :local:
      :backlinks: None

   Code -- shebang
   ---------------

   ::

      #!/usr/bin/env

Example 2
---------

.. code-block::

    doc = RstCloth(line_width=180)
    doc.title('Example Document')
    doc.newline()
    doc.table(
        ['Column 1', 'Column 2', 'Column 3'],
        data=[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    )

    doc.print_content()


Contents:

.. toctree::
   :maxdepth: 2

   rstcloth


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

