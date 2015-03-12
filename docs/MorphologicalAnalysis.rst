
Morphological Analysis
======================

.. code:: python

    import sys
    import os.path as p
.. code:: python

    %load_ext autoreload
    %autoreload 2
.. code:: python

    exp_dir = "/media/data/code/polyglot/"
    
    if exp_dir not in sys.path:
      sys.path.insert(0, exp_dir)
.. code:: python

    import polyglot
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
    print(", ".join(sorted(downloader.supported_languages("morph2"))))

.. parsed-literal::

    Afrikaans, Albanian, Alemannic, Amharic, Arabic, Aragonese, Armenian, Assamese, Asturian, Azerbaijani, Bashkir, Basque, Bavarian, Belarusian, Bengali, Bishnupriya Manipuri, Bosnian, Bosnian-Croatian-Serbian, Breton, Bulgarian, Burmese, Catalan; Valencian, Cebuano, Chechen, Chinese, Chuvash, Croatian, Czech, Danish, Divehi; Dhivehi; Maldivian;, Dutch, Egyptian Arabic, English, Esperanto, Estonian, Faroese, Fiji Hindi, Finnish, French, Galician, Gan Chinese, Georgian, German, Greek, Modern, Gujarati, Haitian; Haitian Creole, Hebrew (modern), Hindi, Hungarian, Icelandic, Ido, Ilokano, Indonesian, Interlingua, Irish, Italian, Japanese, Javanese, Kannada, Kapampangan, Kazakh, Khmer, Kirghiz, Kyrgyz, Korean, Kurdish, Latin, Latvian, Limburgish, Limburgan, Limburger, Lithuanian, Lombard language, Luxembourgish, Letzeburgesch, Macedonian, Malagasy, Malay, Malayalam, Maltese, Manx, Marathi (Marāṭhī), Mongolian, Nepali, Northern Sami, Norwegian, Norwegian Nynorsk, Occitan, Oriya, Ossetian, Ossetic, Panjabi, Punjabi, Pashto, Pushto, Persian, Piedmontese language, Polish, Portuguese, Quechua, Romanian, Moldavian, Moldovan, Romansh, Russian, Sakha, Sanskrit (Saṁskṛta), Scots, Scottish Gaelic; Gaelic, Serbian, Sicilian, Silesian, Sinhala, Sinhalese, Slovak, Slovene, Spanish; Castilian, Sundanese, Swahili, Swedish, Tagalog, Tajik, Tamil, Tatar, Telugu, Thai, Tibetan Standard, Tibetan, Central, Turkish, Turkmen, Uighur, Uyghur, Ukrainian, Upper Sorbian, Urdu, Uzbek, Venetian, Vietnamese, Volapük, Walloon, Waray-Waray, Welsh, West Flemish, Western Frisian, Yiddish, Yoruba, Zazaki


Download Necessary Models
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    %%bash
    polyglot download morph2.en morph2.ar

.. parsed-literal::

    [polyglot_data] Downloading package morph2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package morph2.en is already up-to-date!
    [polyglot_data] Downloading package morph2.ar to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package morph2.ar is already up-to-date!


Library Interface
-----------------

We tag each word in the text with one part of speech.

.. code:: python

    from polyglot.text import Text, Word
.. code:: python

    blob = "Wewillmeettoday."
    text = Text(blob)
    text.language = "en"
We can query all the tagged words

.. code:: python

    text.morphemes



.. parsed-literal::

    WordList([u'We', u'will', u'meet', u'to', u'day', u'.'])



After calling the pos\_tags property once, the words objects will carry
the POS tags.

.. code:: python

    words = ["preprocessing", "processor", "invaluable", "thankful", "crossed"]
    for w in words:
      w2 = Word(w, language="en")
      print("{:<20}{}".format(w2, w2.morphemes))

.. parsed-literal::

    preprocessing       ['pre', 'process', 'ing']
    processor           ['process', 'or']
    invaluable          ['in', 'valuable']
    thankful            ['thank', 'ful']
    crossed             ['cross', 'ed']


Command Line Interface
----------------------

Tokenization
^^^^^^^^^^^^

Notice, if we do not pass ``--lang`` the language code, the detector
will bem used to detect the language of the document.

.. code:: python

    %%bash
    tok_file=/tmp/cricket.tok.txt
    polyglot --lang en tokenize --input testdata/cricket.txt > $tok_file
    head -n 2 $tok_file

.. parsed-literal::

    Australia posted a World Cup record total of 417 - 6 as they beat Afghanistan by 275 runs .
    David Warner hit 178 off 133 balls , Steve Smith scored 95 while Glenn Maxwell struck 88 in 39 deliveries in the Pool A encounter in Perth .


Morphemes
^^^^^^^^^

.. code:: python

    %%bash
    tok_file=/tmp/cricket.tok.txt
    polyglot --lang en morph --input $tok_file | tail -n 50

.. parsed-literal::

    -               -    
    4               4    
    against         a_gain_st
    West            West 
    Indies          In_dies
    and             and  
    Ireland         Ireland
    respectively    re_spective_ly
    .               .    
    
    The             The  
    winning         winning
    margin          margin
    beats           beat_s
    the             the  
    257             2_57 
    -               -    
    run             run  
    amount          amount
    by              by   
    which           which
    India           In_dia
    beat            beat 
    Bermuda         Ber_mud_a
    in              in   
    Port            Port 
    of              of   
    Spain           Spa_in
    in              in   
    2007            2007 
    ,               ,    
    which           which
    was             wa_s 
    equalled        equal_led
    five            five 
    days            day_s
    ago             ago  
    by              by   
    South           South
    Africa          Africa
    in              in   
    their           t_heir
    victory         victor_y
    over            over 
    West            West 
    Indies          In_dies
    in              in   
    Sydney          Syd_ney
    .               .    
    


Nesting steps
^^^^^^^^^^^^^

We can nest the tokenization and POS tagging in a simple bash pipeline

.. code:: python

    !polyglot --lang en tokenize --input testdata/cricket.txt |  polyglot --lang en morph | tail -n 30

.. parsed-literal::

    which           which
    India           In_dia
    beat            beat 
    Bermuda         Ber_mud_a
    in              in   
    Port            Port 
    of              of   
    Spain           Spa_in
    in              in   
    2007            2007 
    ,               ,    
    which           which
    was             wa_s 
    equalled        equal_led
    five            five 
    days            day_s
    ago             ago  
    by              by   
    South           South
    Africa          Africa
    in              in   
    their           t_heir
    victory         victor_y
    over            over 
    West            West 
    Indies          In_dies
    in              in   
    Sydney          Syd_ney
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
                Title:	Morfessor 2.0: Python Implementation and Extensions for Morfessor Baseline
                Author(s):	Virpioja, Sami ; Smit, Peter ; Grönroos, Stig-Arne ; Kurimo, Mikko
                Date:	2013
                Language:	en
                Pages:	38
                Department:	Signaalinkäsittelyn ja akustiikan laitos
                Department of Signal Processing and Acoustics
                ISBN:	978-952-60-5501-5 (electronic)
                Series:	Aalto University publication series SCIENCE + TECHNOLOGY, 25/2013
                ISSN:	1799-490X (electronic)
                1799-4896 (printed)
                1799-4896 (ISSN-L)
                Subject:	Computer science, Linguistics
                Keywords:	morpheme segmentation, morphology induction, unsupervised learning, semi-supervised learning, morfessor, machine learning
   }
References
----------

-  `Universal Part of Speech
   Tagging <http://universaldependencies.github.io/docs/u/pos/index.html>`__
-  `Universal Dependencies
   1.0 <https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1464>`__.
