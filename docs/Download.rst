
Downloading Models
==================

Polyglot requires a model for each task and language. These models are
essential for the library to function. Given the large size of some of
the models, we distribute the models through a download manager
separately. The download manager has several models of operation.

Modes of Operations
-------------------

Interactive Mode Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !polyglot download

.. parsed-literal::

    Polyglot Downloader
    ---------------------------------------------------------------------------
      d) Download   l) List    u) Update   c) Config   h) Help   q) Quit
    ---------------------------------------------------------------------------
    Downloader> 

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !polyglot download --help

.. parsed-literal::

    usage: polyglot download [-h] [--dir DIR] [--quiet] [--force] [--exit-on-error] [--url SERVER_INDEX_URL] [packages [packages ...]]
    
    positional arguments:
      packages              packages to be downloaded
    
    optional arguments:
      -h, --help            show this help message and exit
      --dir DIR             download package to directory DIR
      --quiet               work quietly
      --force               download even if already installed
      --exit-on-error       exit if an error occurs
      --url SERVER_INDEX_URL
                            download server index url


.. code:: python

    !polyglot download morph2.en

.. parsed-literal::

    [polyglot_data] Downloading package morph2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package morph2.en is already up-to-date!


Library Interface
~~~~~~~~~~~~~~~~~

.. code:: python

    from polyglot.downloader import downloader
    downloader.download("embeddings2.en")

.. parsed-literal::

    [polyglot_data] Downloading package embeddings2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package embeddings2.en is already up-to-date!




.. parsed-literal::

    True



Collections
-----------

You noticed by now that we can install a specific model by specifying
its name and the target language.

Package name format is ``task_name.language_code``

Langauge Collections
^^^^^^^^^^^^^^^^^^^^

Packages are grouped by language. For example, if we want to download
all the models that are specific to Arabic, the arabic collection of
models name is **LANG:** followed by the language code of Arabic which
is ``ar``.

Therefore, we can just run:

.. code:: python

    !polyglot download LANG:ar

.. parsed-literal::

    [polyglot_data] Downloading collection u'LANG:ar'
    [polyglot_data]    | 
    [polyglot_data]    | Downloading package tsne2.ar to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    | Downloading package transliteration2.ar to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ar is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package morph2.ar to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package morph2.ar is already up-to-date!
    [polyglot_data]    | Downloading package counts2.ar to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    | Downloading package sentiment2.ar to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    | Downloading package embeddings2.ar to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    | Downloading package ner2.ar to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package ner2.ar is already up-to-date!
    [polyglot_data]    | 
    [polyglot_data]  Done downloading collection LANG:ar


Task Collections
^^^^^^^^^^^^^^^^

Packages are grouped by task. For example, if we want to download all
the models that perform transliteration. The collection name is
**TASK:** followed by the task name.

Therefore, we can just run:

.. code:: python

    downloader.download("TASK:transliteration2")

.. parsed-literal::

    [polyglot_data] Downloading collection u'TASK:transliteration2'
    [polyglot_data]    | 
    [polyglot_data]    | Downloading package transliteration2.nn to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.nn is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.no to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.no is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.nl to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.nl is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.az to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.az is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ar to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ar is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.am to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.am is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.id to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.id is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.af to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.af is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ta to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ta is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ja to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ja is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.sq to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.sq is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.sr to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.sr is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.sw to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.sw is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.sv to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.sv is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.zh to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.zh is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.sh to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.sh is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.sl to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.sl is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.da to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.da is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.mk to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.mk is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ms to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ms is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.mt to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.mt is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.de to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.de is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.gl to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.gl is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.hr to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.hr is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.it to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.it is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.is to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.is is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.bg to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.bg is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.be to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.be is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ht to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ht is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.uk to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.uk is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ur to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ur is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.mr to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.mr is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ru to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ru is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.he to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.he is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ro to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ro is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ko to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ko is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.vi to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.vi is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.gu to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.gu is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ga to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ga is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.hu to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.hu is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.hy to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.hy is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.hi to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.hi is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.fr to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.fr is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ca to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ca is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.fa to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.fa is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.cs to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.cs is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.cy to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.cy is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.te to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.te is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.th to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.th is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.tl to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.tl is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.tr to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.tr is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.la to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.la is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.fi to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.fi is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.lt to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.lt is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.lv to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.lv is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.pl to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.pl is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.pt to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.pt is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.yi to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.yi is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.bn to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.bn is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.bs to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.bs is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.km to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.km is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.kn to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.kn is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.ka to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.ka is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.sk to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.sk is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.eu to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.eu is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.es to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.es is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.et to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.et is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.eo to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.eo is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | Downloading package transliteration2.el to
    [polyglot_data]    |     /home/rmyeid/polyglot_data...
    [polyglot_data]    |   Package transliteration2.el is already up-to-
    [polyglot_data]    |       date!
    [polyglot_data]    | 
    [polyglot_data]  Done downloading collection TASK:transliteration2




.. parsed-literal::

    True



Langauge & Task Support
-----------------------

We can query our download manager for which tasks are supported by
polyglot, as the following:

.. code:: python

    downloader.supported_tasks(lang="en")



.. parsed-literal::

    [u'embeddings2',
     u'counts2',
     u'pos2',
     u'ner2',
     u'sentiment2',
     u'morph2',
     u'tsne2']



We can query our download manager for which languages are supported by
polyglot named entity recognition subsystem, as the following:

.. code:: python

    downloader.supported_languages(task="ner2")



.. parsed-literal::

    ['Polish',
     'Turkish',
     'Russian',
     'Indonesian',
     'Czech',
     'Arabic',
     'Korean',
     'Catalan; Valencian',
     'Italian',
     'Thai',
     'Romanian, Moldavian, Moldovan',
     'Tagalog',
     'Danish',
     'Finnish',
     'German',
     'Persian',
     'Dutch',
     'Chinese',
     'French',
     'Portuguese',
     'Slovak',
     'Hebrew (modern)',
     'Malay',
     'Slovene',
     'Bulgarian',
     'Hindi',
     'Japanese',
     'Hungarian',
     'Croatian',
     'Ukrainian',
     'Serbian',
     'Lithuanian',
     'Norwegian',
     'Latvian',
     'Swedish',
     'English',
     'Greek, Modern',
     'Spanish; Castilian',
     'Vietnamese',
     'Estonian']



You can view all the downloaded packages and available ones in the index
through the list function

.. code:: python

    downloader.list(show_packages=False)

.. parsed-literal::

    Using default data directory (/home/rmyeid/polyglot_data)
    =========================================
     Data server index for <polyglot-models>
    =========================================
    Collections:
      [ ] LANG:af............. Afrikaans            packages and models
      [ ] LANG:als............ als                  packages and models
      [ ] LANG:am............. Amharic              packages and models
      [ ] LANG:an............. Aragonese            packages and models
      [ ] LANG:ar............. Arabic               packages and models
      [ ] LANG:arz............ arz                  packages and models
      [ ] LANG:as............. Assamese             packages and models
      [ ] LANG:ast............ Asturian             packages and models
      [ ] LANG:az............. Azerbaijani          packages and models
      [ ] LANG:ba............. Bashkir              packages and models
      [ ] LANG:bar............ bar                  packages and models
      [ ] LANG:be............. Belarusian           packages and models
      [ ] LANG:bg............. Bulgarian            packages and models
      [ ] LANG:bn............. Bengali              packages and models
      [ ] LANG:bo............. Tibetan              packages and models
      [ ] LANG:bpy............ bpy                  packages and models
      [ ] LANG:br............. Breton               packages and models
      [ ] LANG:bs............. Bosnian              packages and models
      [ ] LANG:ca............. Catalan              packages and models
      [ ] LANG:ce............. Chechen              packages and models
      [ ] LANG:ceb............ Cebuano              packages and models
      [ ] LANG:cs............. Czech                packages and models
      [ ] LANG:cv............. Chuvash              packages and models
      [ ] LANG:cy............. Welsh                packages and models
      [ ] LANG:da............. Danish               packages and models
      [ ] LANG:de............. German               packages and models
      [ ] LANG:diq............ diq                  packages and models
      [ ] LANG:dv............. Divehi               packages and models
      [ ] LANG:el............. Greek                packages and models
      [P] LANG:en............. English              packages and models
      [ ] LANG:eo............. Esperanto            packages and models
      [ ] LANG:es............. Spanish              packages and models
      [ ] LANG:et............. Estonian             packages and models
      [ ] LANG:eu............. Basque               packages and models
      [ ] LANG:fa............. Persian              packages and models
      [ ] LANG:fi............. Finnish              packages and models
      [ ] LANG:fo............. Faroese              packages and models
      [ ] LANG:fr............. French               packages and models
      [ ] LANG:fy............. Western Frisian      packages and models
      [ ] LANG:ga............. Irish                packages and models
      [ ] LANG:gan............ gan                  packages and models
      [ ] LANG:gd............. Scottish Gaelic      packages and models
      [ ] LANG:gl............. Galician             packages and models
      [ ] LANG:gu............. Gujarati             packages and models
      [ ] LANG:gv............. Manx                 packages and models
      [ ] LANG:he............. Hebrew               packages and models
      [ ] LANG:hi............. Hindi                packages and models
      [ ] LANG:hif............ hif                  packages and models
      [ ] LANG:hr............. Croatian             packages and models
      [ ] LANG:hsb............ Upper Sorbian        packages and models
      [ ] LANG:ht............. Haitian              packages and models
      [ ] LANG:hu............. Hungarian            packages and models
      [ ] LANG:hy............. Armenian             packages and models
      [ ] LANG:ia............. Interlingua          packages and models
      [ ] LANG:id............. Indonesian           packages and models
      [ ] LANG:ilo............ Iloko                packages and models
      [ ] LANG:io............. Ido                  packages and models
      [ ] LANG:is............. Icelandic            packages and models
      [ ] LANG:it............. Italian              packages and models
      [ ] LANG:ja............. Japanese             packages and models
      [ ] LANG:jv............. Javanese             packages and models
      [ ] LANG:ka............. Georgian             packages and models
      [ ] LANG:kk............. Kazakh               packages and models
      [ ] LANG:km............. Khmer                packages and models
      [ ] LANG:kn............. Kannada              packages and models
      [ ] LANG:ko............. Korean               packages and models
      [ ] LANG:ku............. Kurdish              packages and models
      [ ] LANG:ky............. Kyrgyz               packages and models
      [ ] LANG:la............. Latin                packages and models
      [ ] LANG:lb............. Luxembourgish        packages and models
      [ ] LANG:li............. Limburgish           packages and models
      [ ] LANG:lmo............ lmo                  packages and models
      [ ] LANG:lt............. Lithuanian           packages and models
      [ ] LANG:lv............. Latvian              packages and models
      [ ] LANG:mg............. Malagasy             packages and models
      [ ] LANG:mk............. Macedonian           packages and models
      [ ] LANG:ml............. Malayalam            packages and models
      [ ] LANG:mn............. Mongolian            packages and models
      [ ] LANG:mr............. Marathi              packages and models
      [ ] LANG:ms............. Malay                packages and models
      [ ] LANG:mt............. Maltese              packages and models
      [ ] LANG:my............. Burmese              packages and models
      [ ] LANG:ne............. Nepali               packages and models
      [ ] LANG:nl............. Dutch                packages and models
      [ ] LANG:nn............. Norwegian Nynorsk    packages and models
      [ ] LANG:no............. Norwegian            packages and models
      [ ] LANG:oc............. Occitan              packages and models
      [ ] LANG:or............. Oriya                packages and models
      [ ] LANG:os............. Ossetic              packages and models
      [ ] LANG:pa............. Punjabi              packages and models
      [ ] LANG:pam............ Pampanga             packages and models
      [ ] LANG:pl............. Polish               packages and models
      [ ] LANG:pms............ pms                  packages and models
      [ ] LANG:ps............. Pashto               packages and models
      [ ] LANG:pt............. Portuguese           packages and models
      [ ] LANG:qu............. Quechua              packages and models
      [ ] LANG:rm............. Romansh              packages and models
      [ ] LANG:ro............. Romanian             packages and models
      [ ] LANG:ru............. Russian              packages and models
      [ ] LANG:sa............. Sanskrit             packages and models
      [ ] LANG:sah............ Sakha                packages and models
      [ ] LANG:scn............ Sicilian             packages and models
      [ ] LANG:sco............ Scots                packages and models
      [ ] LANG:se............. Northern Sami        packages and models
      [ ] LANG:sh............. Serbo-Croatian       packages and models
      [ ] LANG:si............. Sinhala              packages and models
      [ ] LANG:sk............. Slovak               packages and models
      [ ] LANG:sl............. Slovenian            packages and models
      [ ] LANG:sq............. Albanian             packages and models
      [ ] LANG:sr............. Serbian              packages and models
      [ ] LANG:su............. Sundanese            packages and models
      [ ] LANG:sv............. Swedish              packages and models
      [ ] LANG:sw............. Swahili              packages and models
      [ ] LANG:szl............ szl                  packages and models
      [ ] LANG:ta............. Tamil                packages and models
      [ ] LANG:te............. Telugu               packages and models
      [ ] LANG:tg............. Tajik                packages and models
      [ ] LANG:th............. Thai                 packages and models
      [ ] LANG:tk............. Turkmen              packages and models
      [ ] LANG:tl............. Tagalog              packages and models
      [ ] LANG:tr............. Turkish              packages and models
      [ ] LANG:tt............. Tatar                packages and models
      [ ] LANG:ug............. Uyghur               packages and models
      [ ] LANG:uk............. Ukrainian            packages and models
      [ ] LANG:ur............. Urdu                 packages and models
      [ ] LANG:uz............. Uzbek                packages and models
      [ ] LANG:vec............ vec                  packages and models
      [ ] LANG:vi............. Vietnamese           packages and models
      [ ] LANG:vls............ vls                  packages and models
      [ ] LANG:vo............. Volapük              packages and models
      [ ] LANG:wa............. Walloon              packages and models
      [ ] LANG:war............ Waray                packages and models
      [ ] LANG:yi............. Yiddish              packages and models
      [ ] LANG:yo............. Yoruba               packages and models
      [ ] LANG:zh............. Chinese              packages and models
      [ ] LANG:zhc............ Chinese Character    packages and models
      [ ] LANG:zhw............ zhw                  packages and models
      [ ] TASK:counts2........ counts2
      [ ] TASK:embeddings2.... embeddings2
      [ ] TASK:ner2........... ner2
      [P] TASK:sentiment2..... sentiment2
      [ ] TASK:tsne2.......... tsne2
    
    ([*] marks installed packages; [P] marks partially installed collections)

