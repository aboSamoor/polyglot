
polyglot
========

|Downloads| |Latest Version| |Supported Python versions| |Development
Status| |Download Format| |Build Status| |Documentation Status|

.. |Downloads| image:: https://pypip.in/download/polyglot/badge.svg
   :target: https://pypi.python.org/pypi/polyglot
.. |Latest Version| image:: https://pypip.in/version/polyglot/badge.svg
   :target: https://pypi.python.org/pypi/polyglot
.. |Supported Python versions| image:: https://pypip.in/py_versions/polyglot/badge.svg
   :target: https://pypi.python.org/pypi/polyglot/
.. |Development Status| image:: https://pypip.in/status/polyglot/badge.svg
   :target: https://pypi.python.org/pypi/polyglot/
.. |Download Format| image:: https://pypip.in/format/polyglot/badge.svg
   :target: https://pypi.python.org/pypi/polyglot
.. |Build Status| image:: https://travis-ci.org/aboSamoor/polyglot.png?branch=master
   :target: https://travis-ci.org/aboSamoor/polyglot
.. |Documentation Status| image:: https://readthedocs.org/projects/polyglot/badge/?version=latest
   :target: https://readthedocs.org/builds/polyglot/

Polyglot is a natural language pipeline that supports massive
multilingual applications.

-  Free software: GPLv3 license
-  Documentation: http://polyglot.readthedocs.org.

Features
~~~~~~~~

-  Tokenization (165 Languages)
-  Language detection (196 Languages)
-  Named Entity Recognition (40 Languages)
-  Sentiment Analysis (136 Languages)
-  Word Embeddings (137 Languages)
-  Morphological analysis (135 Languages)
-  Transliteration (69 Languages)

Developer
~~~~~~~~~

-  Rami Al-Rfou @ ``rmyeid gmail com``

Qiuck Tutorial
--------------

.. code:: python

    import polyglot
    from polyglot.text import Text

Language Detection
~~~~~~~~~~~~~~~~~~

.. code:: python

    text = Text("Bonjour, Mesdames.")
    print("Language Detected: Code={}, Name={}\n".format(text.language.code, text.language.name))


.. parsed-literal::

    Language Detected: Code=fr, Name=French
    


Tokenization
~~~~~~~~~~~~

.. code:: python

    zen = Text("Beautiful is better than ugly. "
               "Explicit is better than implicit. "
               "Simple is better than complex.")
    print(zen.words)


.. parsed-literal::

    [u'Beautiful', u'is', u'better', u'than', u'ugly', u'.', u'Explicit', u'is', u'better', u'than', u'implicit', u'.', u'Simple', u'is', u'better', u'than', u'complex', u'.']


.. code:: python

    print(zen.sentences)


.. parsed-literal::

    [Sentence("Beautiful is better than ugly."), Sentence("Explicit is better than implicit."), Sentence("Simple is better than complex.")]


Part of Speech Tagging
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    text = Text(u"O primeiro uso de desobediência civil em massa ocorreu em setembro de 1906.")
    
    print("{:<16}{}".format("Word", "POS Tag")+"\n"+"-"*30)
    for word, tag in text.pos_tags:
        print(u"{:<16}{:>2}".format(word, tag))


.. parsed-literal::

    Word            POS Tag
    ------------------------------
    O               PART
    primeiro        SCONJ
    uso             PART
    de              ADP
    desobediência   PART
    civil           SCONJ
    em              ADP
    massa           PART
    ocorreu         SCONJ
    em              ADP
    setembro        PART
    de              ADP
    1906            DET
    .               ADV


Named Entity Recognition
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    text = Text(u"In Großbritannien war Gandhi mit dem westlichen Lebensstil vertraut geworden")
    print(text.entities)


.. parsed-literal::

    [I-LOC([u'Gro\xdfbritannien']), I-PER([u'Gandhi'])]


Polarity
~~~~~~~~

.. code:: python

    print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
    for w in zen.words[:6]:
        print("{:<16}{:>2}".format(w, w.polarity))


.. parsed-literal::

    Word            Polarity
    ------------------------------
    Beautiful        0
    is               0
    better           1
    than             0
    ugly            -1
    .                0


Embeddings
~~~~~~~~~~

.. code:: python

    word = zen.words[0]
    print(word.vector)


.. parsed-literal::

    [-0.08001513 -0.35475096  0.27702546 -0.20423636  0.36313248  0.06376412
      0.0444247  -0.30489922  0.014972    0.13951094  0.07515849 -0.2703914
      0.04650182  0.58747977  0.5101701  -0.04114699  0.37434807 -0.27707747
     -0.06124159  0.21493433 -0.23498166  0.07404013 -0.23953673 -0.15044802
      0.21210277 -0.58776855  0.12014424  0.30591646  0.07079886  0.44168213
      0.2473582  -0.43409103 -0.25516582  0.45812422  0.33660468  0.61951864
      0.16038296 -0.12069689 -0.59378242 -0.47525382 -0.03109539  0.28781402
     -0.51556301 -0.26363477 -0.0820123   0.31425434 -0.10971891  0.53333962
      0.3446033  -0.62146574 -0.15398794  0.11720303  0.50415224 -0.79616308
     -0.25548786  0.36809164 -0.26254281  0.11736908 -0.30717522 -0.18103991
     -0.03320931 -0.15692121 -0.22654058  0.56092978]


Morphology
~~~~~~~~~~

.. code:: python

    word = Text("Preprocessing is an essential step.").words[0]
    print(word.morphemes)


.. parsed-literal::

    [u'Pre', u'process', u'ing']


Transliteration
~~~~~~~~~~~~~~~

.. code:: python

    from polyglot.transliteration import Transliterator
    transliterator = Transliterator(source_lang="en", target_lang="ru")
    print(transliterator.transliterate(u"preprocessing"))


.. parsed-literal::

    препрокессинг

