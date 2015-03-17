
Transliteration
===============

Transliteration is the conversion of a text from one script to another.
For instance, a Latin transliteration of the Greek phrase "Ελληνική
Δημοκρατία", usually translated as 'Hellenic Republic', is "Ellēnikḗ
Dēmokratía".

.. code:: python

    from polyglot.transliteration import Transliterator
Languages Coverage
------------------

**TODO**

Describe how did we get these models

.. code:: python

    from __future__ import print_function
.. code:: python

    from polyglot.downloader import downloader
    print(", ".join(downloader.supported_languages("pos2")))
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

    for x in text.transliterate("ar"):
      print(x)

.. parsed-literal::

    وي
    ويل
    ميت
    ات
    ييايت
    أوكلوك
    ون
    ثورسداي
    مورنينغ
    


Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !polyglot --lang en tokenize --input testdata/cricket.txt |  polyglot --lang en transliteration --target ar | tail -n 30

.. parsed-literal::

    which           ويكه            
    India           ينديا           
    beat            بيت             
    Bermuda         بيرمودا         
    in              ين              
    Port            بورت            
    of              وف              
    Spain           سباين           
    in              ين              
    2007                            
    ,                               
    which           ويكه            
    was             واس             
    equalled        يكالليد         
    five            فيفي            
    days            دايس            
    ago             اغو             
    by              بي              
    South           سووث            
    Africa          افريكا          
    in              ين              
    their           ثير             
    victory         فيكتوري         
    over            وفير            
    West            ويست            
    Indies          يندييس          
    in              ين              
    Sydney          سيدني           
    .                               
    


Citation
~~~~~~~~

This work is a direct implementation of the research being described in
the `FooBar <https://abc.com>`__ paper. The author of this library
strongly encourage you to cite the following paper if you are using this
software.

::

References
----------

-  asd
-  asd
