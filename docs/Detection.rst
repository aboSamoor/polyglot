
Language Detection
==================

Polyglot depends on `pycld2 <https://pypi.python.org/pypi/pycld2/>`__
library which in turn depends on
`cld2 <https://code.google.com/p/cld2/>`__ library for detecting
language(s) used in plain text.

.. code:: python

    from polyglot.detect import Detector

Example
-------

.. code:: python

    arabic_text = u"""
    أفاد مصدر امني في قيادة عمليات صلاح الدين في العراق بأن " القوات الامنية تتوقف لليوم
    الثالث على التوالي عن التقدم الى داخل مدينة تكريت بسبب
    انتشار قناصي التنظيم الذي يطلق على نفسه اسم "الدولة الاسلامية" والعبوات الناسفة
    والمنازل المفخخة والانتحاريين، فضلا عن ان القوات الامنية تنتظر وصول تعزيزات اضافية ".
    """


.. code:: python

    detector = Detector(arabic_text)
    print(detector.language)


.. parsed-literal::

    name: Arabic      code: ar       confidence:  99.0 read bytes:   907


Mixed Text
----------

.. code:: python

    mixed_text = u"""
    China (simplified Chinese: 中国; traditional Chinese: 中國),
    officially the People's Republic of China (PRC), is a sovereign state located in East Asia.
    """

If the text contains snippets from different languages, the detector is
able to find the most probable langauges used in the text. For each
language, we can query the model confidence level:

.. code:: python

    for language in Detector(mixed_text).languages:
      print(language)


.. parsed-literal::

    name: English     code: en       confidence:  87.0 read bytes:  1154
    name: Chinese     code: zh_Hant  confidence:   5.0 read bytes:  1755
    name: un          code: un       confidence:   0.0 read bytes:     0


To take a closer look, we can inspect the text line by line, notice that
the confidence in the detection went down for the first line

.. code:: python

    for line in mixed_text.strip().splitlines():
      print(line + u"\n")
      for language in Detector(line).languages:
        print(language)
      print("\n")


.. parsed-literal::

    China (simplified Chinese: 中国; traditional Chinese: 中國),
    
    name: English     code: en       confidence:  71.0 read bytes:   887
    name: Chinese     code: zh_Hant  confidence:  11.0 read bytes:  1755
    name: un          code: un       confidence:   0.0 read bytes:     0
    
    
    officially the People's Republic of China (PRC), is a sovereign state located in East Asia.
    
    name: English     code: en       confidence:  98.0 read bytes:  1291
    name: un          code: un       confidence:   0.0 read bytes:     0
    name: un          code: un       confidence:   0.0 read bytes:     0
    
    


Best Effort Strategy
--------------------

Sometimes, there is no enough text to make a decision, like detecting a
language from one word. This forces the detector to switch to a best
effort strategy, a warning will be thrown and the attribute ``reliable``
will be set to ``False``.

.. code:: python

    detector = Detector("pizza")
    print(detector)


.. parsed-literal::

    WARNING:polyglot.detect.base:Detector is not able to detect the language reliably.


.. parsed-literal::

    Prediction is reliable: False
    Language 1: name: English     code: en       confidence:  85.0 read bytes:  1194
    Language 2: name: un          code: un       confidence:   0.0 read bytes:     0
    Language 3: name: un          code: un       confidence:   0.0 read bytes:     0


In case, that the detection is not reliable even when we are using the
best effort strategy, an exception ``UnknownLanguage`` will be thrown.

.. code:: python

    print(Detector("4"))


::


    ---------------------------------------------------------------------------

    UnknownLanguage                           Traceback (most recent call last)

    <ipython-input-9-de43776398b9> in <module>()
    ----> 1 print(Detector("4"))
    

    /usr/local/lib/python2.7/dist-packages/polyglot-15.04.17-py2.7.egg/polyglot/detect/base.pyc in __init__(self, text, quiet)
         63     self.quiet = quiet
         64     """If true, exceptions will be silenced."""
    ---> 65     self.detect(text)
         66 
         67   @staticmethod


    /usr/local/lib/python2.7/dist-packages/polyglot-15.04.17-py2.7.egg/polyglot/detect/base.pyc in detect(self, text)
         89 
         90       if not reliable and not self.quiet:
    ---> 91         raise UnknownLanguage("Try passing a longer snippet of text")
         92       else:
         93         logger.warning("Detector is not able to detect the language reliably.")


    UnknownLanguage: Try passing a longer snippet of text


Such an exception may not be desirable especially for trivial cases like
characters that could belong to so many languages. In this case, we can
silence the exceptions by passing setting ``quiet`` to ``True``

.. code:: python

    print(Detector("4", quiet=True))


.. parsed-literal::

    WARNING:polyglot.detect.base:Detector is not able to detect the language reliably.


.. parsed-literal::

    Prediction is reliable: False
    Language 1: name: un          code: un       confidence:   0.0 read bytes:     0
    Language 2: name: un          code: un       confidence:   0.0 read bytes:     0
    Language 3: name: un          code: un       confidence:   0.0 read bytes:     0


Command Line
------------

.. code:: python

    !polyglot detect --help


.. parsed-literal::

    usage: polyglot detect [-h] [--input [INPUT [INPUT ...]]]
    
    optional arguments:
      -h, --help            show this help message and exit
      --input [INPUT [INPUT ...]]


The subcommand ``detect`` tries to identify the language code for each
line in a text file. This could be convieniet if each line represents a
document or a sentence that could have been generated by a tokenizer

.. code:: python

    !polyglot detect --input testdata/cricket.txt


.. parsed-literal::

    English             Australia posted a World Cup record total of 417-6 as they beat Afghanistan by 275 runs.
    English             David Warner hit 178 off 133 balls, Steve Smith scored 95 while Glenn Maxwell struck 88 in 39 deliveries in the Pool A encounter in Perth.
    English             Afghanistan were then dismissed for 142, with Mitchell Johnson and Mitchell Starc taking six wickets between them.
    English             Australia's score surpassed the 413-5 India made against Bermuda in 2007.
    English             It continues the pattern of bat dominating ball in this tournament as the third 400 plus score achieved in the pool stages, following South Africa's 408-5 and 411-4 against West Indies and Ireland respectively.
    English             The winning margin beats the 257-run amount by which India beat Bermuda in Port of Spain in 2007, which was equalled five days ago by South Africa in their victory over West Indies in Sydney.


Supported Languages
-------------------

cld2 can detect up to 165 languages.

.. code:: python

    from polyglot.utils import pretty_list
    print(pretty_list(Detector.supported_languages()))


.. parsed-literal::

      1. Abkhazian                  2. Afar                       3. Afrikaans                
      4. Akan                       5. Albanian                   6. Amharic                  
      7. Arabic                     8. Armenian                   9. Assamese                 
     10. Aymara                    11. Azerbaijani               12. Bashkir                  
     13. Basque                    14. Belarusian                15. Bengali                  
     16. Bihari                    17. Bislama                   18. Bosnian                  
     19. Breton                    20. Bulgarian                 21. Burmese                  
     22. Catalan                   23. Cebuano                   24. Cherokee                 
     25. Nyanja                    26. Corsican                  27. Croatian                 
     28. Croatian                  29. Czech                     30. Chinese                  
     31. Chinese                   32. Chinese                   33. Chinese                  
     34. Chineset                  35. Chineset                  36. Chineset                 
     37. Chineset                  38. Chineset                  39. Chineset                 
     40. Danish                    41. Dhivehi                   42. Dutch                    
     43. Dzongkha                  44. English                   45. Esperanto                
     46. Estonian                  47. Ewe                       48. Faroese                  
     49. Fijian                    50. Finnish                   51. French                   
     52. Frisian                   53. Ga                        54. Galician                 
     55. Ganda                     56. Georgian                  57. German                   
     58. Greek                     59. Greenlandic               60. Guarani                  
     61. Gujarati                  62. Haitian_creole            63. Hausa                    
     64. Hawaiian                  65. Hebrew                    66. Hebrew                   
     67. Hindi                     68. Hmong                     69. Hungarian                
     70. Icelandic                 71. Igbo                      72. Indonesian               
     73. Interlingua               74. Interlingue               75. Inuktitut                
     76. Inupiak                   77. Irish                     78. Italian                  
     79. Ignore                    80. Javanese                  81. Javanese                 
     82. Japanese                  83. Kannada                   84. Kashmiri                 
     85. Kazakh                    86. Khasi                     87. Khmer                    
     88. Kinyarwanda               89. Krio                      90. Kurdish                  
     91. Kyrgyz                    92. Korean                    93. Laothian                 
     94. Latin                     95. Latvian                   96. Limbu                    
     97. Limbu                     98. Limbu                     99. Lingala                  
    100. Lithuanian               101. Lozi                     102. Luba_lulua               
    103. Luo_kenya_and_tanzania   104. Luxembourgish            105. Macedonian               
    106. Malagasy                 107. Malay                    108. Malayalam                
    109. Maltese                  110. Manx                     111. Maori                    
    112. Marathi                  113. Mauritian_creole         114. Romanian                 
    115. Mongolian                116. Montenegrin              117. Montenegrin              
    118. Montenegrin              119. Montenegrin              120. Nauru                    
    121. Ndebele                  122. Nepali                   123. Newari                   
    124. Norwegian                125. Norwegian                126. Norwegian_n              
    127. Nyanja                   128. Occitan                  129. Oriya                    
    130. Oromo                    131. Ossetian                 132. Pampanga                 
    133. Pashto                   134. Pedi                     135. Persian                  
    136. Polish                   137. Portuguese               138. Punjabi                  
    139. Quechua                  140. Rajasthani               141. Rhaeto_romance           
    142. Romanian                 143. Rundi                    144. Russian                  
    145. Samoan                   146. Sango                    147. Sanskrit                 
    148. Scots                    149. Scots_gaelic             150. Serbian                  
    151. Serbian                  152. Seselwa                  153. Seselwa                  
    154. Sesotho                  155. Shona                    156. Sindhi                   
    157. Sinhalese                158. Siswant                  159. Slovak                   
    160. Slovenian                161. Somali                   162. Spanish                  
    163. Sundanese                164. Swahili                  165. Swedish                  
    166. Syriac                   167. Tagalog                  168. Tajik                    
    169. Tamil                    170. Tatar                    171. Telugu                   
    172. Thai                     173. Tibetan                  174. Tigrinya                 
    175. Tonga                    176. Tsonga                   177. Tswana                   
    178. Tumbuka                  179. Turkish                  180. Turkmen                  
    181. Twi                      182. Uighur                   183. Ukrainian                
    184. Urdu                     185. Uzbek                    186. Venda                    
    187. Vietnamese               188. Volapuk                  189. Waray_philippines        
    190. Welsh                    191. Wolof                    192. Xhosa                    
    193. Yiddish                  194. Yoruba                   195. Zhuang                   
    196. Zulu                     

