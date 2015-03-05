
Part of Speech tagging
======================

Part of speech tagging task aims to assign every word/token in plain
text a category that identifies the syntactic functionality of the word
occurrence.

Polyglot recognizes 17 parts of speech:

-  **ADJ**: adjective
-  **ADP**: adposition
-  **ADV**: adverb
-  **AUX**: auxiliary verb
-  **CONJ**: coordinating conjunction
-  **DET**: determiner
-  **INTJ**: interjection
-  **NOUN**: noun
-  **NUM**: numeral
-  **PART**: particle
-  **PRON**: pronoun
-  **PROPN**: proper noun
-  **PUNCT**: punctuation
-  **SCONJ**: subordinating conjunction
-  **SYM**: symbol
-  **VERB**: verb
-  **X**: other

Languages Coverage
------------------

The models were trained on a combination of: - Original CONLL datasets
after the tags were converted using the `universal POS
tables <http://universaldependencies.github.io/docs/tagset-conversion/index.html>`__.
- Universal Dependencies 1.0 corpora whenever they are available.

.. code:: python

    from __future__ import print_function
.. code:: python

    from polyglot.downloader import downloader
    print(", ".join(downloader.supported_languages("pos2")))

.. parsed-literal::

    Danish, Czech, Slovene, English, Bulgarian, Swedish, Portuguese, Dutch


Download Necessary Models
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    %%bash
    polyglot download embeddings2.en pos2.en

.. parsed-literal::

    [polyglot_data] Downloading package embeddings2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package embeddings2.en is already up-to-date!
    [polyglot_data] Downloading package pos2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package pos2.en is already up-to-date!


Library Interface
-----------------

We tag each word in the text with one part of speech.

.. code:: python

    from polyglot.text import Text
.. code:: python

    blob = """We will meet at eight o'clock on Thursday morning."""
    text = Text(blob)
We can query all the tagged words

.. code:: python

    text.pos_tags



.. parsed-literal::

    [(u'We', u'PRON'),
     (u'will', u'VERB'),
     (u'meet', u'VERB'),
     (u'at', u'ADP'),
     (u'eight', u'NUM'),
     (u"o'clock", u'NOUN'),
     (u'on', u'ADP'),
     (u'Thursday', u'NOUN'),
     (u'morning', u'NOUN'),
     (u'.', u'.')]



After calling the pos\_tags property once, the words objects will carry
the POS tags.

.. code:: python

    text.words[0].pos_tag



.. parsed-literal::

    u'PRON'



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

    2015-03-05 17:21:22 INFO __main__.py: 246 Language English is detected while reading the first 1128 bytes.


Part of Speech
^^^^^^^^^^^^^^

.. code:: python

    %%bash
    tok_file=/tmp/cricket.tok.txt
    polyglot --lang en pos --input $tok_file | head -n 25

.. parsed-literal::

    Australia       NOUN 
    posted          VERB 
    a               DET  
    World           NOUN 
    Cup             NOUN 
    record          NOUN 
    total           NOUN 
    of              ADP  
    417             NOUN 
    -               .    
    6               NOUN 
    as              ADP  
    they            PRON 
    beat            VERB 
    Afghanistan     NOUN 
    by              ADP  
    275             NOUN 
    runs            NOUN 
    .               .    
    
    David           NOUN 
    Warner          NOUN 
    hit             VERB 
    178             ADJ  
    off             ADP  


Nesting steps
^^^^^^^^^^^^^

We can nest the tokenization and POS tagging in a simple bash pipeline

.. code:: python

    !polyglot --lang en tokenize --input testdata/cricket.txt |  polyglot --lang en pos | tail -n 30

.. parsed-literal::

    which           DET  
    India           NOUN 
    beat            VERB 
    Bermuda         NOUN 
    in              ADP  
    Port            NOUN 
    of              ADP  
    Spain           NOUN 
    in              ADP  
    2007            NOUN 
    ,               .    
    which           DET  
    was             VERB 
    equalled        VERB 
    five            NUM  
    days            NOUN 
    ago             ADV  
    by              ADP  
    South           NOUN 
    Africa          NOUN 
    in              ADP  
    their           PRON 
    victory         NOUN 
    over            ADP  
    West            NOUN 
    Indies          NOUN 
    in              ADP  
    Sydney          NOUN 
    .               .    
    


Citation
~~~~~~~~

This work is a direct implementation of the research being described in
the `Polyglot: Distributed Word Representations for Multilingual
NLP <http://www.aclweb.org/anthology/W13-3520>`__ paper. The author of
this library strongly encourage you to cite the following paper if you
are using this software.
.. code-block::
   @InProceedings{polyglot:2013:ACL-CoNLL,
     author    = {Al-Rfou, Rami  and  Perozzi, Bryan  and  Skiena, Steven},
     title     = {Polyglot: Distributed Word Representations for Multilingual NLP},
     booktitle = {Proceedings of the Seventeenth Conference on Computational Natural Language Learning},
     month     = {August},
     year      = {2013},
     address   = {Sofia, Bulgaria},
     publisher = {Association for Computational Linguistics},
     pages     = {183--192}, 
     url       = {http://www.aclweb.org/anthology/W13-3520}
   }
References
----------

-  `Universal Part of Speech
   Tagging <http://universaldependencies.github.io/docs/u/pos/index.html>`__
-  `Universal Dependencies
   1.0 <https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1464>`__.
