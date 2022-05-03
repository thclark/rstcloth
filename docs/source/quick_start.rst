.. _quick_start:

============
Quick Start
============

Example 1
---------

The following RstCloth code:

.. code-block:: python

   from rstcloth import RstCloth

   with open('my.rst', 'w') as output_file:
       doc = RstCloth(output_file)
       doc.title('Example Use')
       doc.newline()
       doc.h2('Contents')
       doc.table_of_contents()
       doc.newline()
       doc.h2('Code -- shebang')
       doc.codeblock('#!/usr/bin/env')

Would result in the following reStructuredText: ::

   ===========
   Example Use
   ===========

   Contents
   --------
   .. contents::
      :backlinks: none

   Code -- shebang
   ---------------
   ::
      #!/usr/bin/env


Example 2
---------

The following RstCloth code:

.. code-block:: python

   from rstcloth import RstCloth

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

Would result in the following reStructuredText: ::

    ================
    Example Document
    ================


    +------------+------------+------------+
    | Column 1   | Column 2   | Column 3   |
    +============+============+============+
    | 1          | 2          | 3          |
    +------------+------------+------------+
    | 4          | 5          | 6          |
    +------------+------------+------------+
    | 7          | 8          | 9          |
    +------------+------------+------------+
