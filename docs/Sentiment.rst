
Sentiment
=========

Polyglot has polarity lexicons for 136 languages. The scale of the
words' polarity consisted of three degrees: +1 for positive words, and
-1 for negatives words. Neutral words will have a score of 0.

Languages Coverage
~~~~~~~~~~~~~~~~~~

.. code:: python

    from polyglot.downloader import downloader
    print(downloader.supported_languages_table("sentiment2", 3))


.. parsed-literal::

      1. Turkmen                    2. Thai                       3. Latvian                  
      4. Zazaki                     5. Tagalog                    6. Tamil                    
      7. Tajik                      8. Telugu                     9. Luxembourgish, Letzeb... 
     10. Alemannic                 11. Latin                     12. Turkish                  
     13. Limburgish, Limburgan...  14. Egyptian Arabic           15. Tatar                    
     16. Lithuanian                17. Spanish; Castilian        18. Basque                   
     19. Estonian                  20. Asturian                  21. Greek, Modern            
     22. Esperanto                 23. English                   24. Ukrainian                
     25. Marathi (Marāṭhī)         26. Maltese                   27. Burmese                  
     28. Kapampangan               29. Uighur, Uyghur            30. Uzbek                    
     31. Malagasy                  32. Yiddish                   33. Macedonian               
     34. Urdu                      35. Malayalam                 36. Mongolian                
     37. Breton                    38. Bosnian                   39. Bengali                  
     40. Tibetan Standard, Tib...  41. Belarusian                42. Bulgarian                
     43. Bashkir                   44. Vietnamese                45. Volapük                  
     46. Gan Chinese               47. Manx                      48. Gujarati                 
     49. Yoruba                    50. Occitan                   51. Scottish Gaelic; Gaelic  
     52. Irish                     53. Galician                  54. Ossetian, Ossetic        
     55. Oriya                     56. Walloon                   57. Swedish                  
     58. Silesian                  59. Lombard language          60. Divehi; Dhivehi; Mald... 
     61. Danish                    62. German                    63. Armenian                 
     64. Haitian; Haitian Creole   65. Hungarian                 66. Croatian                 
     67. Bishnupriya Manipuri      68. Hindi                     69. Hebrew (modern)          
     70. Portuguese                71. Afrikaans                 72. Pashto, Pushto           
     73. Amharic                   74. Aragonese                 75. Bavarian                 
     76. Assamese                  77. Panjabi, Punjabi          78. Polish                   
     79. Azerbaijani               80. Italian                   81. Arabic                   
     82. Icelandic                 83. Ido                       84. Scots                    
     85. Sicilian                  86. Indonesian                87. Chinese Word             
     88. Interlingua               89. Waray-Waray               90. Piedmontese language     
     91. Quechua                   92. French                    93. Dutch                    
     94. Norwegian Nynorsk         95. Norwegian                 96. Western Frisian          
     97. Upper Sorbian             98. Nepali                    99. Persian                  
    100. Ilokano                  101. Finnish                  102. Faroese                  
    103. Romansh                  104. Javanese                 105. Romanian, Moldavian, ... 
    106. Malay                    107. Japanese                 108. Russian                  
    109. Catalan; Valencian       110. Fiji Hindi               111. Chinese                  
    112. Cebuano                  113. Czech                    114. Chuvash                  
    115. Welsh                    116. West Flemish             117. Kirghiz, Kyrgyz          
    118. Kurdish                  119. Kazakh                   120. Korean                   
    121. Kannada                  122. Khmer                    123. Georgian                 
    124. Sakha                    125. Serbian                  126. Albanian                 
    127. Swahili                  128. Chechen                  129. Sundanese                
    130. Sanskrit (Saṁskṛta)      131. Venetian                 132. Northern Sami            
    133. Slovak                   134. Sinhala, Sinhalese       135. Bosnian-Croatian-Serbian 
    136. Slovene                  


.. code:: python

    from polyglot.text import Text

Polarity
--------

To inquiry the polarity of a word, we can just call its own attribute
``polarity``

.. code:: python

    text = Text("The movie was really good.")

.. code:: python

    print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
    for w in text.words:
        print("{:<16}{:>2}".format(w, w.polarity))


.. parsed-literal::

    Word            Polarity
    ------------------------------
    The              0
    movie            0
    was              0
    really           0
    good             1
    .                0


Entity Sentiment
----------------

We can calculate a more sphosticated sentiment score for an entity that
is mentioned in text as the following:

.. code:: python

    blob = ("Barack Obama gave a fantastic speech last night. "
            "Reports indicate he will move next to New Hampshire.")
    text = Text(blob)

First, we need split the text into sentneces, this will limit the words
tha affect the sentiment of an entity to the words mentioned in the
sentnece.

.. code:: python

    first_sentence = text.sentences[0]
    print(first_sentence)


.. parsed-literal::

    The movie was really good.


Second, we extract the entities

.. code:: python

    first_entity = first_sentence.entities[0]
    print(first_entity)


.. parsed-literal::

    [u'Obama']


Finally, for each entity we identified, we can calculate the strength of
the positive or negative sentiment it has on a scale from 0-1

.. code:: python

    first_entity.positive_sentiment




.. parsed-literal::

    0.9375



.. code:: python

    first_entity.negative_sentiment




.. parsed-literal::

    0



Citation
~~~~~~~~

This work is a direct implementation of the research being described in
the `Building sentiment lexicons for all major
languages <http://aclweb.org/anthology/P14-2063>`__ paper. The author of
this library strongly encourage you to cite the following paper if you
are using this software.

::

       @inproceedings{chen2014building,
       title={Building sentiment lexicons for all major languages},
       author={Chen, Yanqing and Skiena, Steven},
       booktitle={Proceedings of the 52nd Annual Meeting of the Association for Computational Linguistics (Short Papers)},
       pages={383--389},
       year={2014}}
