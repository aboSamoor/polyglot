
Part of Speech Tagging
======================

Part of speech tagging task aims to assign every word/token in plain
text a category that identifies the syntactic functionality of the word
occurrence.

Polyglot recognizes 17 parts of speech, this set is called the
``universal part of speech tag set``:

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

The models were trained on a combination of:

-  Original CONLL datasets after the tags were converted using the
   `universal POS
   tables <http://universaldependencies.github.io/docs/tagset-conversion/index.html>`__.

-  Universal Dependencies 1.0 corpora whenever they are available.

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


Example
-------

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
~~~~~~~~~~~~~~~~~~~~~~

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

::

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
