.. :changelog:

History
-------

"14.11" (2014-01-11)
---------------------

* First release on PyPI.


"15.5.2" (2015-05-02)
---------------------

* Polyglot is feature complete.


"15.10.03" (2015-10-03)
---------------------------

* Change the polyglot models mirror to Stony Brook University DSL lab instead
  of Google cloud storage.


"16.07.04" (2016-07-03)
---------------------------

* New Features:
  - Support Transfer POS Tagging.
  - Support supplying `hint_language_code` for `Text`.

* Bug Fix: 
  - Improve sentence serialization (PR #34)
  - Fix rare unicode encode error (PR #35)
  - Fix transliteration from languages other than English (PR 46)
  - Add link to Github in README (PR #49)
  - Make handling of paths more coherent (RP #55)
  - Fix normalizing embedding in place for NER corrupts the features of POS (issue #60, PR #62)

