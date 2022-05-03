.. _quick_start:

============
Quick Start
============

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

   print(str(d))

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

    print(str(doc))

Would result in the following reStructuredText: ::

    ================
    Example Document
    ================


    +-----------+-----------+-----------+
    |Column 1   |Column 2   |Column 3   |
    +===========+===========+===========+
    |1          |2          |3          |
    +-----------+-----------+-----------+
    |4          |5          |6          |
    +-----------+-----------+-----------+
    |7          |8          |9          |
    +-----------+-----------+-----------+

