
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

    from polyglot.downloader import downloader
    print(downloader.supported_languages_table("morph2"))


.. parsed-literal::

      1. Piedmontese language       2. Lombard language           3. Gan Chinese              
      4. Sicilian                   5. Scots                      6. Kirghiz, Kyrgyz          
      7. Pashto, Pushto             8. Kurdish                    9. Portuguese               
     10. Kannada                   11. Korean                    12. Khmer                    
     13. Kazakh                    14. Ilokano                   15. Polish                   
     16. Panjabi, Punjabi          17. Georgian                  18. Chuvash                  
     19. Alemannic                 20. Czech                     21. Welsh                    
     22. Chechen                   23. Catalan; Valencian        24. Northern Sami            
     25. Sanskrit (Saṁskṛta)       26. Slovene                   27. Javanese                 
     28. Slovak                    29. Bosnian-Croatian-Serbian  30. Bavarian                 
     31. Swedish                   32. Swahili                   33. Sundanese                
     34. Serbian                   35. Albanian                  36. Japanese                 
     37. Western Frisian           38. French                    39. Finnish                  
     40. Upper Sorbian             41. Faroese                   42. Persian                  
     43. Sinhala, Sinhalese        44. Italian                   45. Amharic                  
     46. Aragonese                 47. Volapük                   48. Icelandic                
     49. Sakha                     50. Afrikaans                 51. Indonesian               
     52. Interlingua               53. Azerbaijani               54. Ido                      
     55. Arabic                    56. Assamese                  57. Yoruba                   
     58. Yiddish                   59. Waray-Waray               60. Croatian                 
     61. Hungarian                 62. Haitian; Haitian Creole   63. Quechua                  
     64. Armenian                  65. Hebrew (modern)           66. Silesian                 
     67. Hindi                     68. Divehi; Dhivehi; Mald...  69. German                   
     70. Danish                    71. Occitan                   72. Tagalog                  
     73. Turkmen                   74. Thai                      75. Tajik                    
     76. Greek, Modern             77. Telugu                    78. Tamil                    
     79. Oriya                     80. Ossetian, Ossetic         81. Tatar                    
     82. Turkish                   83. Kapampangan               84. Venetian                 
     85. Manx                      86. Gujarati                  87. Galician                 
     88. Irish                     89. Scottish Gaelic; Gaelic   90. Nepali                   
     91. Cebuano                   92. Zazaki                    93. Walloon                  
     94. Dutch                     95. Norwegian                 96. Norwegian Nynorsk        
     97. West Flemish              98. Chinese                   99. Bosnian                  
    100. Breton                   101. Belarusian               102. Bulgarian                
    103. Bashkir                  104. Egyptian Arabic          105. Tibetan Standard, Tib... 
    106. Bengali                  107. Burmese                  108. Romansh                  
    109. Marathi (Marāṭhī)        110. Malay                    111. Maltese                  
    112. Russian                  113. Macedonian               114. Malayalam                
    115. Mongolian                116. Malagasy                 117. Vietnamese               
    118. Spanish; Castilian       119. Estonian                 120. Basque                   
    121. Bishnupriya Manipuri     122. Asturian                 123. English                  
    124. Esperanto                125. Luxembourgish, Letzeb... 126. Latin                    
    127. Uighur, Uyghur           128. Ukrainian                129. Limburgish, Limburgan... 
    130. Latvian                  131. Urdu                     132. Lithuanian               
    133. Fiji Hindi               134. Uzbek                    135. Romanian, Moldavian, ... 
    


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
