
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

.. code:: python

    from polyglot.downloader import downloader
    print(downloader.supported_languages_table("transliteration2"))


.. parsed-literal::

      1. Haitian; Haitian Creole    2. Tamil                      3. Vietnamese               
      4. Telugu                     5. Croatian                   6. Hungarian                
      7. Thai                       8. Kannada                    9. Tagalog                  
     10. Armenian                  11. Hebrew (modern)           12. Turkish                  
     13. Portuguese                14. Belarusian                15. Norwegian Nynorsk        
     16. Norwegian                 17. Dutch                     18. Japanese                 
     19. Albanian                  20. Bulgarian                 21. Serbian                  
     22. Swahili                   23. Swedish                   24. French                   
     25. Latin                     26. Czech                     27. Yiddish                  
     28. Hindi                     29. Danish                    30. Finnish                  
     31. German                    32. Bosnian-Croatian-Serbian  33. Slovak                   
     34. Persian                   35. Lithuanian                36. Slovene                  
     37. Latvian                   38. Bosnian                   39. Gujarati                 
     40. Italian                   41. Icelandic                 42. Spanish; Castilian       
     43. Ukrainian                 44. Georgian                  45. Urdu                     
     46. Indonesian                47. Marathi (Marāṭhī)         48. Korean                   
     49. Galician                  50. Khmer                     51. Catalan; Valencian       
     52. Romanian, Moldavian, ...  53. Basque                    54. Macedonian               
     55. Russian                   56. Azerbaijani               57. Chinese                  
     58. Estonian                  59. Welsh                     60. Arabic                   
     61. Bengali                   62. Amharic                   63. Irish                    
     64. Malay                     65. Afrikaans                 66. Polish                   
     67. Greek, Modern             68. Esperanto                 69. Maltese                  
    


Downloading Necessary Models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    %%bash
    polyglot download embeddings2.en transliteration2.ar


.. parsed-literal::

    [polyglot_data] Downloading package embeddings2.en to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package embeddings2.en is already up-to-date!
    [polyglot_data] Downloading package transliteration2.ar to
    [polyglot_data]     /home/rmyeid/polyglot_data...
    [polyglot_data]   Package transliteration2.ar is already up-to-date!


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
    

