
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

    from polyglot.downloader import downloader
    print(downloader.supported_languages_table("ner2", 3))


.. parsed-literal::

      1. Polish                     2. Turkish                    3. Russian                  
      4. Indonesian                 5. Czech                      6. Arabic                   
      7. Korean                     8. Catalan; Valencian         9. Italian                  
     10. Thai                      11. Romanian, Moldavian, ...  12. Tagalog                  
     13. Danish                    14. Finnish                   15. German                   
     16. Persian                   17. Dutch                     18. Chinese                  
     19. French                    20. Portuguese                21. Slovak                   
     22. Hebrew (modern)           23. Malay                     24. Slovene                  
     25. Bulgarian                 26. Hindi                     27. Japanese                 
     28. Hungarian                 29. Croatian                  30. Ukrainian                
     31. Serbian                   32. Lithuanian                33. Norwegian                
     34. Latvian                   35. Swedish                   36. English                  
     37. Greek, Modern             38. Spanish; Castilian        39. Vietnamese               
     40. Estonian                 


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


Example
-------

Entities inside a text object or a sentence are represented as chunks.
Each chunk identifies the start and the end indices of the word
subsequence within the text.

.. code:: python

    from polyglot.text import Text

.. code:: python

    blob = """The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world"."""
    text = Text(blob)
    
    # We can also specify language of that text by using
    # text = Text(blob, hint_language_code='en')

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
~~~~~~~~~~~~~~~~~~~~~~

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
   <embed>
   <iframe src="https://entityextractor.appspot.com/" width="100%" height="225" seamless></iframe>
   </embed>

Citation
~~~~~~~~

This work is a direct implementation of the research being described in
the `Polyglot-NER: Multilingual Named Entity
Recognition <https://sites.google.com/site/rmyeid/papers/polyglot-ner.pdf?attredirects=0&d=1>`__
paper. The author of this library strongly encourage you to cite the
following paper if you are using this software.

::

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
