
polyglot
========

|Downloads| |Latest Version| |Build Status| |Documentation Status|

.. |Downloads| image:: https://img.shields.io/pypi/dm/polyglot.svg
   :target: https://pypi.python.org/pypi/polyglot
.. |Latest Version| image:: https://badge.fury.io/py/polyglot.svg
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
-  Part of Speech Tagging (16 Languages)
-  Sentiment Analysis (136 Languages)
-  Word Embeddings (137 Languages)
-  Morphological analysis (135 Languages)
-  Transliteration (69 Languages)

Developer
~~~~~~~~~

-  Rami Al-Rfou @ ``rmyeid gmail com``

Quick Tutorial
--------------

.. code:: python

    import polyglot
    from polyglot.text import Text, Word

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
    O               DET
    primeiro        ADJ
    uso             NOUN
    de              ADP
    desobediência   NOUN
    civil           ADJ
    em              ADP
    massa           NOUN
    ocorreu         ADJ
    em              ADP
    setembro        NOUN
    de              ADP
    1906            NUM
    .               PUNCT


Named Entity Recognition
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    text = Text(u"In Großbritannien war Gandhi mit dem westlichen Lebensstil vertraut geworden")
    print(text.entities)


.. parsed-literal::

    [I-LOC([u'Gro\\xdfbritannien']), I-PER([u'Gandhi'])]


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

    word = Word("Obama", language="en")
    print("Neighbors (Synonms) of {}".format(word)+"\n"+"-"*30)
    for w in word.neighbors:
        print("{:<16}".format(w))
    print("\n\nThe first 10 dimensions out the {} dimensions\n".format(word.vector.shape[0]))
    print(word.vector[:10])


.. parsed-literal::

    Neighbors (Synonms) of Obama
    ------------------------------
    Bush            
    Reagan          
    Clinton         
    Ahmadinejad     
    Nixon           
    Karzai          
    McCain          
    Biden           
    Huckabee        
    Lula            
    
    
    The first 10 dimensions out the 256 dimensions
    
    [-2.57382345  1.52175975  0.51070285  1.08678675 -0.74386948 -1.18616164
      2.92784619 -0.25694436 -1.40958667 -2.39675403]


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

