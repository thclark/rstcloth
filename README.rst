==========================
RstCloth -- Project README
==========================

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

Status
------

RstCloth is undergoing ongoing development and expansion is not
stable at this point. Current features and projects include:

- improve documentation.

- develop unit testing framework to ensure consistent API behavior.
  
- build/extend a table generation API.
  
- improve paragraph level content generation API.

See the `issue tracker
<https://issues.cyborginstitute.net/buglist.cgi?cmdtype=runnamed&namedcmd=rstcloth>`_
for a more complete list of current and future projects.

Project
-------

Source repository: the `canonical git.cyborginstitute.net repository
<http://git.cyborginstitute.net/?p=rstcloth.git;a=summary>`_ has a
`github mirror <https://github.com/cyborginstitute/rstcloth>`_.

Issue tracker: `cyborg institute bugzilla
<https://issues.cyborginstitute.net/buglist.cgi?cmdtype=runnamed&namedcmd=rstcloth>`_.

Listserv: `cyborg institute listserv
<http://lists.cyborginstitute.net/listinfo/institute>`_.
