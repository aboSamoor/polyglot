
Transliteration
===============

.. code:: python

    import sys
    import os.path as p
.. code:: python

    %load_ext autoreload
    %autoreload 2
.. code:: python

    exp_dir = '/media/data/code/polyglot/'
    if exp_dir not in sys.path:
      sys.path.insert(0, exp_dir)
.. code:: python

    import polyglot
.. code:: python

    from polyglot.load import load_transliteration_table, locate_resource
.. code:: python

    from polyglot.transliteration import Transliterator
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

    2015-03-11 22:20:03 INFO __main__.py: 275 Language English is detected while reading the first 1128 bytes.


Part of Speech
^^^^^^^^^^^^^^

.. code:: python

    %%bash
    tok_file=/tmp/cricket.tok.txt
    polyglot --lang en transliteration --target ar --input $tok_file | head -n 25

.. parsed-literal::

    Australia       اوستراليا       
    posted          بوستيد          
    a               ا               
    World           وورلد           
    Cup             كوب             
    record          ريكورد          
    total           توتال           
    of              وف              
    417                             
    -                               
    6                               
    as              اس              
    they            ثي              
    beat            بيت             
    Afghanistan     افغانيستان      
    by              بي              
    275                             
    runs            رونس            
    .                               
    
    David           دافيد           
    Warner          وارنر           
    hit             هيت             
    178                             
    off             وفف             


Nesting steps
^^^^^^^^^^^^^

We can nest the tokenization and POS tagging in a simple bash pipeline

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
the `Polyglot: Distributed Word Representations for Multilingual
NLP <http://www.aclweb.org/anthology/W13-3520>`__ paper. The author of
this library strongly encourage you to cite the following paper if you
are using this software.
.. code-block::
References
----------

-  `Universal Part of Speech
   Tagging <http://universaldependencies.github.io/docs/u/pos/index.html>`__
-  `Universal Dependencies
   1.0 <https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1464>`__.
