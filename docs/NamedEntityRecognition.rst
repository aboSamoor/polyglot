
Named Entity Extraction
=======================

Named entity extraction task aims to extract phrases from plain text
that correpond to entities. Polyglot recognizes 3 categories of
entities:

-  Locations (Tag: ``I-LOC``): cities, countries, regions, continents,
   neighborhoods, administrative divisions ...
-  Organizations (Tag: ``I-ORG``): sports teams, newspapers, banks,
   universities, schools, non-profits, companies, ...
-  Persons (Tag: ``I-PER``): politicians, scientists, artists, atheletes
   ...

Languages Coverage
------------------

The models were trained on datasets extracted automatically from
Wikipedia. Polyglot currently supports 40 major languages.

.. code:: python

    from __future__ import print_function
.. code:: python

    from polyglot.downloader import downloader
    print(", ".join(downloader.supported_languages("ner2")))

.. parsed-literal::

    Polish, Turkish, Russian, Czech, Arabic, Korean, Catalan; Valencian, Indonesian, Vietnamese, Thai, Romanian, Moldavian, Moldovan, Tagalog, Danish, Finnish, German, Persian, Latvian, Chinese, French, Portuguese, Slovak, Hebrew (modern), Malay, Slovene, Bulgarian, Hindi, Japanese, Hungarian, Croatian, Ukrainian, Serbian, Lithuanian, Norwegian, Dutch, Swedish, English, Greek, Modern, Spanish; Castilian, Italian, Estonian


Download Necessary Models
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    %%bash
    polyglot download embeddings2.en ner2.en

.. parsed-literal::

    [polyglot_data] Downloading package embeddings2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package embeddings2.en is already up-to-date!
    [polyglot_data] Downloading package ner2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package ner2.en is already up-to-date!


Library Interface
-----------------

Entities inside a text object or a sentence are represented as chunks.
Each chunk identifies the start and the end indices of the word
subsequence within the text.

.. code:: python

    from polyglot.text import Text
.. code:: python

    blob = """The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world"."""
    text = Text(blob)
We can query all entities mentioned in a text.

.. code:: python

    text.entities



.. parsed-literal::

    [I-ORG([u'Israeli']), I-PER([u'Benjamin', u'Netanyahu']), I-LOC([u'Iran'])]



Or, we can query entites per sentence

.. code:: python

    for sent in text.sentences:
      print(sent, "\n")
      for entity in sent.entities:
        print(entity.tag, entity)

.. parsed-literal::

    The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world". 
    
    I-ORG [u'Israeli']
    I-PER [u'Benjamin', u'Netanyahu']
    I-LOC [u'Iran']


By doing more careful inspection of the second entity
``Benjamin Netanyahu``, we can locate the position of the entity within
the sentence.

.. code:: python

    benjamin = sent.entities[1]
    sent.words[benjamin.start: benjamin.end]



.. parsed-literal::

    WordList([u'Benjamin', u'Netanyahu'])



Command Line Interface
----------------------

Tokenization
^^^^^^^^^^^^

Notice, if we do not pass ``--lang`` the language code, the detector
will bem used to detect the language of the document.

.. code:: python

    %%bash
    tok_file=/tmp/cricket.tok.txt
    polyglot tokenize --input testdata/cricket.txt > $tok_file
    head -n 2 $tok_file

.. parsed-literal::

    Australia posted a World Cup record total of 417 - 6 as they beat Afghanistan by 275 runs .
    David Warner hit 178 off 133 balls , Steve Smith scored 95 while Glenn Maxwell struck 88 in 39 deliveries in the Pool A encounter in Perth .


.. parsed-literal::

    2015-03-05 17:27:39 INFO __main__.py: 246 Language English is detected while reading the first 1128 bytes.


Named Entity Extraction
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    %%bash
    tok_file=/tmp/cricket.tok.txt
    polyglot --lang en ner --input $tok_file | head -n 20

.. parsed-literal::

    Australia       I-LOC
    posted          O    
    a               O    
    World           O    
    Cup             O    
    record          O    
    total           O    
    of              O    
    417             O    
    -               O    
    6               O    
    as              O    
    they            O    
    beat            O    
    Afghanistan     I-LOC
    by              O    
    275             O    
    runs            O    
    .               O    
    


Nesting steps
^^^^^^^^^^^^^

We can nest the tokenization and the named entity extraction in a simple
bash pipeline

.. code:: python

    !polyglot --lang en tokenize --input testdata/cricket.txt |  polyglot --lang en ner | tail -n 20

.. parsed-literal::

    ,               O    
    which           O    
    was             O    
    equalled        O    
    five            O    
    days            O    
    ago             O    
    by              O    
    South           I-LOC
    Africa          I-LOC
    in              O    
    their           O    
    victory         O    
    over            O    
    West            I-ORG
    Indies          I-ORG
    in              O    
    Sydney          I-LOC
    .               O    
    


Demo
----
.. raw:: html
   <iframe src="https://entityextractor.appspot.com/" width="100%" height="225" seamless></iframe>

Citation
--------

This work is a direct implementation of the research being described in
the `Polyglot-NER: Multilingual Named Entity
Recognition <https://sites.google.com/site/rmyeid/papers/polyglot-ner.pdf?attredirects=0&d=1>`__
paper. The author of this library strongly encourage you to cite the
following paper if you are using this software.
.. code-block::
   @article{polyglotner,
            author = {Al-Rfou, Rami and Kulkarni, Vivek and Perozzi, Bryan and Skiena, Steven},
            title = {{Polyglot-NER}: Massive Multilingual Named Entity Recognition},
            journal = {{Proceedings of the 2015 {SIAM} International Conference on Data Mining, Vancouver, British Columbia, Canada, April 30 - May 2, 2015}},
            month     = {April},
            year      = {2015},
            publisher = {SIAM}
   }
References
----------

-  `Polyglot-NER project page. <https://bit.ly/polyglot-ner>`__
-  `Wikipedia on
   NER <http://en.wikipedia.org/wiki/Named-entity_recognition>`__.
