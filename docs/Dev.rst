
.. code:: python

    import sys
    from os import path as p

.. code:: python

    polyglot_dir = '/data/polyglot/'
    
    if polyglot_dir not in sys.path:
      sys.path.insert(0, polyglot_dir)

.. code:: python

    %load_ext autoreload
    %autoreload 2


.. parsed-literal::

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload


.. code:: python

    import polyglot
    from polyglot.text import Text

Download packages
=================

.. code:: python

    from polyglot.downloader import download, list_packages, _downloader
    download(info_or_id=u"sentiment2.en")


.. parsed-literal::

    [polyglot_data] Downloading package sentiment2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package sentiment2.en is already up-to-date!




.. parsed-literal::

    True



.. code:: python

    bla = _downloader._collections["en"]
    bla.children




.. parsed-literal::

    [<Package tsne2.en>,
     <Package sentiment2.en>,
     <Package counts2.en>,
     <Package embeddings2.en>,
     <Package ner2.en>]



.. code:: python

    list_packages()


.. parsed-literal::

    Using default data directory (/home/rmyeid/polyglot_data)
    =========================================
     Data server index for <polyglot-models>
    =========================================
    Collections:
      [P] lang:af............. Afrikaans            packages and models
      [P] lang:als............ als                  packages and models
      [P] lang:am............. Amharic              packages and models
      [P] lang:an............. Aragonese            packages and models
      [P] lang:ar............. Arabic               packages and models
      [P] lang:arz............ arz                  packages and models
      [P] lang:as............. Assamese             packages and models
      [P] lang:ast............ Asturian             packages and models
      [P] lang:az............. Azerbaijani          packages and models
      [P] lang:ba............. Bashkir              packages and models
      [P] lang:bar............ bar                  packages and models
      [P] lang:be............. Belarusian           packages and models
      [P] lang:bg............. Bulgarian            packages and models
      [P] lang:bn............. Bengali              packages and models
      [P] lang:bo............. Tibetan              packages and models
      [P] lang:bpy............ bpy                  packages and models
      [P] lang:br............. Breton               packages and models
      [P] lang:bs............. Bosnian              packages and models
      [P] lang:ca............. Catalan              packages and models
      [P] lang:ce............. Chechen              packages and models
      [P] lang:ceb............ Cebuano              packages and models
      [P] lang:cs............. Czech                packages and models
      [P] lang:cv............. Chuvash              packages and models
      [P] lang:cy............. Welsh                packages and models
      [P] lang:da............. Danish               packages and models
      [P] lang:de............. German               packages and models
      [P] lang:diq............ diq                  packages and models
      [P] lang:dv............. Divehi               packages and models
      [P] lang:el............. Greek                packages and models
      [P] lang:en............. English              packages and models
      [P] lang:eo............. Esperanto            packages and models
      [P] lang:es............. Spanish              packages and models
      [P] lang:et............. Estonian             packages and models
      [P] lang:eu............. Basque               packages and models
      [P] lang:fa............. Persian              packages and models
      [P] lang:fi............. Finnish              packages and models
      [P] lang:fo............. Faroese              packages and models
      [P] lang:fr............. French               packages and models
      [P] lang:fy............. Western Frisian      packages and models
      [P] lang:ga............. Irish                packages and models
      [P] lang:gan............ gan                  packages and models
      [P] lang:gd............. Scottish Gaelic      packages and models
      [P] lang:gl............. Galician             packages and models
      [P] lang:gu............. Gujarati             packages and models
      [P] lang:gv............. Manx                 packages and models
      [P] lang:he............. Hebrew               packages and models
      [P] lang:hi............. Hindi                packages and models
      [P] lang:hif............ hif                  packages and models
      [P] lang:hr............. Croatian             packages and models
      [P] lang:hsb............ Upper Sorbian        packages and models
      [P] lang:ht............. Haitian              packages and models
      [P] lang:hu............. Hungarian            packages and models
      [P] lang:hy............. Armenian             packages and models
      [P] lang:ia............. Interlingua          packages and models
      [P] lang:id............. Indonesian           packages and models
      [P] lang:ilo............ Iloko                packages and models
      [P] lang:io............. Ido                  packages and models
      [P] lang:is............. Icelandic            packages and models
      [P] lang:it............. Italian              packages and models
      [P] lang:ja............. Japanese             packages and models
      [P] lang:jv............. Javanese             packages and models
      [P] lang:ka............. Georgian             packages and models
      [P] lang:kk............. Kazakh               packages and models
      [P] lang:km............. Khmer                packages and models
      [P] lang:kn............. Kannada              packages and models
      [P] lang:ko............. Korean               packages and models
      [P] lang:ku............. Kurdish              packages and models
      [P] lang:ky............. Kyrgyz               packages and models
      [P] lang:la............. Latin                packages and models
      [P] lang:lb............. Luxembourgish        packages and models
      [P] lang:li............. Limburgish           packages and models
      [P] lang:lmo............ lmo                  packages and models
      [P] lang:lt............. Lithuanian           packages and models
      [P] lang:lv............. Latvian              packages and models
      [P] lang:mg............. Malagasy             packages and models
      [P] lang:mk............. Macedonian           packages and models
      [P] lang:ml............. Malayalam            packages and models
      [P] lang:mn............. Mongolian            packages and models
      [P] lang:mr............. Marathi              packages and models
      [P] lang:ms............. Malay                packages and models
      [P] lang:mt............. Maltese              packages and models
      [P] lang:my............. Burmese              packages and models
      [P] lang:ne............. Nepali               packages and models
      [P] lang:nl............. Dutch                packages and models
      [P] lang:nn............. Norwegian Nynorsk    packages and models
      [P] lang:no............. Norwegian            packages and models
      [P] lang:oc............. Occitan              packages and models
      [P] lang:or............. Oriya                packages and models
      [P] lang:os............. Ossetic              packages and models
      [P] lang:pa............. Punjabi              packages and models
      [P] lang:pam............ Pampanga             packages and models
      [P] lang:pl............. Polish               packages and models
      [P] lang:pms............ pms                  packages and models
      [P] lang:ps............. Pashto               packages and models
      [P] lang:pt............. Portuguese           packages and models
      [P] lang:qu............. Quechua              packages and models
      [P] lang:rm............. Romansh              packages and models
      [P] lang:ro............. Romanian             packages and models
      [P] lang:ru............. Russian              packages and models
      [P] lang:sa............. Sanskrit             packages and models
      [P] lang:sah............ Sakha                packages and models
      [P] lang:scn............ Sicilian             packages and models
      [P] lang:sco............ Scots                packages and models
      [P] lang:se............. Northern Sami        packages and models
      [P] lang:sh............. Serbo-Croatian       packages and models
      [P] lang:si............. Sinhala              packages and models
      [P] lang:sk............. Slovak               packages and models
      [P] lang:sl............. Slovenian            packages and models
      [P] lang:sq............. Albanian             packages and models
      [P] lang:sr............. Serbian              packages and models
      [P] lang:su............. Sundanese            packages and models
      [P] lang:sv............. Swedish              packages and models
      [P] lang:sw............. Swahili              packages and models
      [P] lang:szl............ szl                  packages and models
      [P] lang:ta............. Tamil                packages and models
      [P] lang:te............. Telugu               packages and models
      [P] lang:tg............. Tajik                packages and models
      [P] lang:th............. Thai                 packages and models
      [P] lang:tk............. Turkmen              packages and models
      [P] lang:tl............. Tagalog              packages and models
      [P] lang:tr............. Turkish              packages and models
      [P] lang:tt............. Tatar                packages and models
      [P] lang:ug............. Uyghur               packages and models
      [P] lang:uk............. Ukrainian            packages and models
      [P] lang:ur............. Urdu                 packages and models
      [P] lang:uz............. Uzbek                packages and models
      [P] lang:vec............ vec                  packages and models
      [P] lang:vi............. Vietnamese           packages and models
      [P] lang:vls............ vls                  packages and models
      [P] lang:vo............. Volapük              packages and models
      [P] lang:wa............. Walloon              packages and models
      [P] lang:war............ Waray                packages and models
      [P] lang:yi............. Yiddish              packages and models
      [P] lang:yo............. Yoruba               packages and models
      [P] lang:zh............. Chinese              packages and models
      [ ] lang:zhc............ Chinese Character    packages and models
      [*] lang:zhw............ zhw                  packages and models
      [ ] task:counts2........ counts2
      [P] task:embeddings2.... embeddings2
      [P] task:ner2........... ner2
      [*] task:sentiment2..... sentiment2
      [P] task:tsne2.......... tsne2
    
    ([*] marks installed packages; [P] marks partially installed collections)


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
    [Sentence("Beautiful is better than ugly."), Sentence("Explicit is better than implicit."), Sentence("Simple is better than complex.")]


Polarity
--------

.. code:: python

    %%bash
    polyglot download sentiment2.en


.. parsed-literal::

    [polyglot_data] Downloading package sentiment2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package sentiment2.en is already up-to-date!


Word base polarity
~~~~~~~~~~~~~~~~~~

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


Sentence Level Sentiment
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    for sent in zen.sentences:
      print sent, sent.polarity


.. parsed-literal::

    Beautiful is better than ugly. 0.0
    Explicit is better than implicit. 1.0
    Simple is better than complex. 0.0


Named Entity Extraction
=======================

.. code:: python

    zen.entities




.. parsed-literal::

    []



Embeddings
----------

.. code:: python

    w = zen.words[5]
    w.vector




.. parsed-literal::

    array([ 0.05519063, -0.01371501,  0.4883692 , -0.24165028,  0.15249102,
           -0.5495227 ,  0.27307254,  0.64203113,  0.54172772,  0.05180147,
           -0.45538789, -0.30796388,  0.61745948, -0.41822246, -0.28658321,
            0.74634224,  0.47470608,  0.77453768,  1.19995797,  0.47836885,
           -0.22754097,  0.1432631 , -0.19801912,  0.24440986, -0.37574792,
           -0.14388466,  0.34778944, -0.39550784, -0.01028192,  0.95838851,
            0.35426503,  0.13478422,  0.05386258,  0.36379546, -0.10879917,
           -0.71637553, -0.25026572,  0.07875264,  0.57645911, -0.7738995 ,
            0.52438337,  0.33535531, -0.16611245,  0.43598977,  0.8950882 ,
           -0.20549561,  0.3005766 ,  0.62948579, -0.28185904, -0.15822442,
            0.59155077,  0.21829523,  0.12933102, -0.07546752,  0.19084625,
           -0.45469594, -0.02288984,  0.44011137,  0.10498845,  0.10494279,
            0.22320323, -0.1855296 , -0.03656057, -0.3861219 ], dtype=float32)


