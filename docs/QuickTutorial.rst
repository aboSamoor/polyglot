
.. code:: python

    import sys
    from os import path as p
.. code:: python

    import polyglot
    from polyglot.text import Text
Language Detection
------------------

.. code:: python

    text = Text("Bonjour, Mesdames.")
    print "Text\n", "-"*40, "\n", text
    detected = text.detected_languages
    print
    print "detector:\n", "-"*40, "\n", detected
    print 
    print "top language code\n", "-"*40, "\n", text.language.code
    print
    print "top language name\n", "-"*40, "\n", text.language.name

.. parsed-literal::

    Text
    ---------------------------------------- 
    Bonjour, Mesdames.
    
    detector:
    ---------------------------------------- 
    Language 1: name: French      code: fr   confidence:  94.0 read bytes:  1204
    Language 2: name: un          code: un   confidence:   0.0 read bytes:     0
    Language 3: name: un          code: un   confidence:   0.0 read bytes:     0
    
    top language code
    ---------------------------------------- 
    fr
    
    top language name
    ---------------------------------------- 
    French


Tokenization
------------

.. code:: python

    zen = Text("Beautiful is better than ugly. "
               "Explicit is better than implicit. "
               "Simple is better than complex.")
    print "Text\n", "-"*40, "\n", zen
    detector = zen.language
    print
    print "\nWords\n", "-"*40
    print zen.words
    print "\nSentences\n", "-"*40
    print zen.sentences

.. parsed-literal::

    Text
    ---------------------------------------- 
    Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex.
    
    
    Words
    ----------------------------------------
    [u'Beautiful', u'is', u'better', u'than', u'ugly', u'.', u'Explicit', u'is', u'better', u'than', u'implicit', u'.', u'Simple', u'is', u'better', u'than', u'complex', u'.']
    
    Sentences
    ----------------------------------------
    [Sentence("Beautiful is better than ugly. "), Sentence("Explicit is better than implicit. "), Sentence("Simple is better than complex.")]


Polarity
--------

.. code:: python

    %%bash
    polyglot download sentiment2.en

.. parsed-literal::

    [polyglot_data] Downloading package sentiment2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package sentiment2.en is already up-to-date!


.. code:: python

    print "{:<16}{}".format("Word", "Polarity"),"\n", "-"*40,"\n"
    for w in zen.words:
        print "{:<16}{:>2}".format(w, w.polarity)

.. parsed-literal::

    Word            Polarity 
    ---------------------------------------- 
    
    Beautiful        0
    is               0
    better           1
    than             0
    ugly            -1
    .                0
    Explicit         0
    is               0
    better           1
    than             0
    implicit         0
    .                0
    Simple           0
    is               0
    better           1
    than             0
    complex         -1
    .                0


Named Entity Extration
======================

.. code:: python

    zen.ne

::


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-14-8f48d90c468d> in <module>()
    ----> 1 zen.entities
    

    AttributeError: 'Text' object has no attribute 'entities'


Embeddings
----------

.. code:: python

    w = zen.words[0]
    w.vector



.. parsed-literal::

    array([-0.08001513, -0.35475096,  0.27702546, -0.20423636,  0.36313248,
            0.06376412,  0.0444247 , -0.30489922,  0.014972  ,  0.13951094,
            0.07515849, -0.2703914 ,  0.04650182,  0.58747977,  0.5101701 ,
           -0.04114699,  0.37434807, -0.27707747, -0.06124159,  0.21493433,
           -0.23498166,  0.07404013, -0.23953673, -0.15044802,  0.21210277,
           -0.58776855,  0.12014424,  0.30591646,  0.07079886,  0.44168213,
            0.2473582 , -0.43409103, -0.25516582,  0.45812422,  0.33660468,
            0.61951864,  0.16038296, -0.12069689, -0.59378242, -0.47525382,
           -0.03109539,  0.28781402, -0.51556301, -0.26363477, -0.0820123 ,
            0.31425434, -0.10971891,  0.53333962,  0.3446033 , -0.62146574,
           -0.15398794,  0.11720303,  0.50415224, -0.79616308, -0.25548786,
            0.36809164, -0.26254281,  0.11736908, -0.30717522, -0.18103991,
           -0.03320931, -0.15692121, -0.22654058,  0.56092978], dtype=float32)


