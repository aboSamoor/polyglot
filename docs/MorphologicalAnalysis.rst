
Morphological Analysis
======================

Polyglot offers trained `morfessor
models <http://www.cis.hut.fi/cis/projects/morpho/>`__ to generate
morphemes from words. The goal of the Morpho project is to develop
unsupervised data-driven methods that discover the regularities behind
word forming in natural languages. In particular, Morpho project is
focussing on the discovery of morphemes, which are the primitive units
of syntax, the smallest individually meaningful elements in the
utterances of a language. Morphemes are important in automatic
generation and recognition of a language, especially in languages in
which words may have many different inflected forms.

Languages Coverage
------------------

Using polyglot vocabulary dictionaries, we trained morfessor models on
the most frequent words 50,000 words of each language.

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


Example
-------

Word Segmentation
~~~~~~~~~~~~~~~~~

.. code:: python

    from polyglot.text import Text, Word

.. code:: python

    words = ["preprocessing", "processor", "invaluable", "thankful", "crossed"]
    for w in words:
      w = Word(w, language="en")
      print("{:<20}{}".format(w, w.morphemes))


.. parsed-literal::

    preprocessing       ['pre', 'process', 'ing']
    processor           ['process', 'or']
    invaluable          ['in', 'valuable']
    thankful            ['thank', 'ful']
    crossed             ['cross', 'ed']


Sentence Segmentation
~~~~~~~~~~~~~~~~~~~~~

If the text is not tokenized properly, morphological analysis could
offer a smart of way of splitting the text into its original units.
Here, is an example:

.. code:: python

    blob = "Wewillmeettoday."
    text = Text(blob)
    text.language = "en"

.. code:: python

    text.morphemes




.. parsed-literal::

    WordList([u'We', u'will', u'meet', u'to', u'day', u'.'])



Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

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
    


Demo
----

This demo does not reflect the models supplied by polyglot, however, we
think it is indicative of what you should expect from morfessor

`Demo <http://www.cis.hut.fi/cgi-bin/morpho/nform.cgi>`__

Citation
~~~~~~~~

This is an interface to the implementation being described in the
`Morfessor2.0: Python Implementation and Extensions for Morfessor
Baseline <https://aaltodoc.aalto.fi/bitstream/handle/123456789/11836/isbn9789526055015.pdf?sequence=1>`__
technical report.

::

    @InProceedings{morfessor2,
                   title:{Morfessor 2.0: Python Implementation and Extensions for Morfessor Baseline},
                   author:  {Virpioja, Sami ; Smit, Peter ; Grönroos, Stig-Arne ; Kurimo, Mikko},
                   year: {2013},
                   publisher: {Department of Signal Processing and Acoustics, Aalto University},
                   booktitle:{Aalto University publication series}
    }

References
----------

-  `Morpho project <http://www.cis.hut.fi/cis/projects/morpho/>`__
-  `Background information on morpheme
   discovery <http://www.cis.hut.fi/cis/projects/morpho/problem.shtml>`__.
