
.. code:: python

    import sys
    from os import path as p
.. code:: python

    polyglot_dir = "/media/data/code/polyglot"
    if polyglot_dir not in sys.path:
      sys.path.insert(0, polyglot_dir)
.. code:: python

    import polyglot
    from polyglot.downloader import downloader
.. code:: python

    downloader.supported_tasks(lang="en")



.. parsed-literal::

    [u'tsne2', u'sentiment2', u'counts2', u'embeddings2', u'ner2']



.. code:: python

    print downloader.supported_languages(task="ner2")

.. parsed-literal::

    ['Polish', 'Turkish', 'Russian', 'Czech', 'Arabic', 'Korean', 'Catalan; Valencian', 'Indonesian', 'Vietnamese', 'Thai', 'Romanian, Moldavian, Moldovan', 'Tagalog', 'Danish', 'Finnish', 'German', 'Persian', 'Latvian', 'Chinese', 'French', 'Portuguese', 'Slovak', 'Hebrew (modern)', 'Malay', 'Slovene', 'Bulgarian', 'Hindi', 'Japanese', 'Hungarian', 'Croatian', 'Ukrainian', 'Serbian', 'Lithuanian', 'Norwegian', 'Dutch', 'Swedish', 'English', 'Greek, Modern', 'Spanish; Castilian', 'Italian', 'Estonian']


.. code:: python

    downloader.download(u"sentiment2.en")

.. parsed-literal::

    [polyglot_data] Downloading package sentiment2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package sentiment2.en is already up-to-date!




.. parsed-literal::

    True



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

