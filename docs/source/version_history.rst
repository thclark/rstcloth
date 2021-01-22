.. _version_history:

===============
Version History
===============

Origins
=======

Huge thankyou to Sam Kleiderman (@tychoish) who originated this package and maintained it up to v0.2.6


.. _version_0.0.x:

Up To 0.2.6
===========

Versions up to 0.2.6 were maintained by @tychoish


0.3.0
=====

@thclark took over project, merged outstanding PRs from over the years, tidied up, sorted docs and devops, made tox
tests run.
Begun work of removing Python 2 code.

Still unstable. Pin your versions, people! Versions > 0.9 will adopt proper semver practice.

New Features
------------
#. Basic implementation and early bugfixes and refactoring.
#. Devops and git maintenance.

Backward Incompatible API Changes
---------------------------------
#. n/a (Resetting the library from half a decade of no maintenance - upgrade at your own risk!)

Bug Fixes & Minor Changes
-------------------------
#. n/a (Initial Release)

.. _version_1.0.0:

1.0.0
=====

#. ``rstcloth.rstcloth.RstCloth`` stores ReStructuredText data in a
   stream. Therefore ``rstcloth.cloth`` module was dropped with
   ``Cloth`` base class.
#. ``rstcloth.rstcloth.RstCloth.table`` uses now python-tabulate for
   table rendering. Therefore ``rstcloth.rstcloth.Table`` class was
   dropped.
#. Line wrapping was improved therefore ``wrap`` parameter in
   ``rstcloth.rstcloth.RstCloth.codeblock``,
   ``rstcloth.rstcloth.RstCloth.content``,
   ``rstcloth.rstcloth.RstCloth.definition``,
   ``rstcloth.rstcloth.RstCloth.directive``,
   ``rstcloth.rstcloth.RstCloth.field``,
   ``rstcloth.rstcloth.RstCloth.footnote`` and
   ``rstcloth.rstcloth.RstCloth.li`` methods was removed.
#. ``rstcloth.rstcloth.RstCloth._paragraph`` method was removed.
#. Module ``rstcloth.table`` was removed and so was ``rstable`` console
   script.
#. Added new ``overline`` parameter to ``heading`` method.
#. Support for ``list-table`` and ``contents`` directives were added.
#. Support for 10 admonition directives was added.
#. Support for 12 bibliographic fields was added.
#. Support for page and frame break and spacer was added.
#. Support for transition marker was added.
#. ``rstcloth.rstcloth.RstCloth.newline`` no longer raises an exception
   if ``count`` parameter is not an integer.
#. Documentation expanded and improved.
