
Language Detection
==================

Polyglot depends on `pycld2 <https://pypi.python.org/pypi/pycld2/>`__
library which in turn depends on
`cld2 <https://code.google.com/p/cld2/>`__ library for detecting
language(s) used in plain text.

.. code:: python

    from __future__ import print_function
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
      print(line, "\n")
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

    <ipython-input-8-de43776398b9> in <module>()
    ----> 1 print(Detector("4"))
    

    /usr/local/lib/python2.7/dist-packages/polyglot-15.03.12-py2.7.egg/polyglot/detect/base.pyc in __init__(self, text, quiet)
         63     self.quiet = quiet
         64     """If true, exceptions will be silenced."""
    ---> 65     self.detect(text)
         66 
         67   @staticmethod


    /usr/local/lib/python2.7/dist-packages/polyglot-15.03.12-py2.7.egg/polyglot/detect/base.pyc in detect(self, text)
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

    print("; ".join(Detector.supported_languages()))


.. parsed-literal::

    Abkhazian; Afar; Afrikaans; Akan; Albanian; Amharic; Arabic; Armenian; Assamese; Aymara; Azerbaijani; Bashkir; Basque; Belarusian; Bengali; Bihari; Bislama; Bosnian; Breton; Bulgarian; Burmese; Catalan; Cebuano; Cherokee; Nyanja; Corsican; Croatian; Croatian; Czech; Chinese; Chinese; Chinese; Chinese; Chineset; Chineset; Chineset; Chineset; Chineset; Chineset; Danish; Dhivehi; Dutch; Dzongkha; English; Esperanto; Estonian; Ewe; Faroese; Fijian; Finnish; French; Frisian; Ga; Galician; Ganda; Georgian; German; Greek; Greenlandic; Guarani; Gujarati; Haitian_creole; Hausa; Hawaiian; Hebrew; Hebrew; Hindi; Hmong; Hungarian; Icelandic; Igbo; Indonesian; Interlingua; Interlingue; Inuktitut; Inupiak; Irish; Italian; Ignore; Javanese; Javanese; Japanese; Kannada; Kashmiri; Kazakh; Khasi; Khmer; Kinyarwanda; Krio; Kurdish; Kyrgyz; Korean; Laothian; Latin; Latvian; Limbu; Limbu; Limbu; Lingala; Lithuanian; Lozi; Luba_lulua; Luo_kenya_and_tanzania; Luxembourgish; Macedonian; Malagasy; Malay; Malayalam; Maltese; Manx; Maori; Marathi; Mauritian_creole; Romanian; Mongolian; Montenegrin; Montenegrin; Montenegrin; Montenegrin; Nauru; Ndebele; Nepali; Newari; Norwegian; Norwegian; Norwegian_n; Nyanja; Occitan; Oriya; Oromo; Ossetian; Pampanga; Pashto; Pedi; Persian; Polish; Portuguese; Punjabi; Quechua; Rajasthani; Rhaeto_romance; Romanian; Rundi; Russian; Samoan; Sango; Sanskrit; Scots; Scots_gaelic; Serbian; Serbian; Seselwa; Seselwa; Sesotho; Shona; Sindhi; Sinhalese; Siswant; Slovak; Slovenian; Somali; Spanish; Sundanese; Swahili; Swedish; Syriac; Tagalog; Tajik; Tamil; Tatar; Telugu; Thai; Tibetan; Tigrinya; Tonga; Tsonga; Tswana; Tumbuka; Turkish; Turkmen; Twi; Uighur; Ukrainian; Urdu; Uzbek; Venda; Vietnamese; Volapuk; Waray_philippines; Welsh; Wolof; Xhosa; X_arabic; X_armenian; X_avestan; X_bork_bork_bork; X_balinese; X_bamum; X_batak; X_bengali; X_bopomofo; X_brahmi; X_braille; X_buginese; X_buhid; X_canadian_aboriginal; X_carian; X_chakma; X_cham; X_cherokee; X_common; X_coptic; X_cuneiform; X_cypriot; X_cyrillic; X_deseret; X_devanagari; X_elmer_fudd; X_egyptian_hieroglyphs; X_ethiopic; X_georgian; X_glagolitic; X_gothic; X_greek; X_gujarati; X_gurmukhi; X_hacker; X_han; X_hangul; X_hanunoo; X_hebrew; X_hiragana; X_imperial_aramaic; X_inherited; X_inscriptional_pahlavi; X_inscriptional_parthian; X_javanese; X_klingon; X_kaithi; X_kannada; X_katakana; X_kayah_li; X_kharoshthi; X_khmer; X_lao; X_latin; X_lepcha; X_limbu; X_linear_b; X_lisu; X_lycian; X_lydian; X_malayalam; X_mandaic; X_meetei_mayek; X_meroitic_cursive; X_meroitic_hieroglyphs; X_miao; X_mongolian; X_myanmar; X_new_tai_lue; X_nko; X_ogham; X_ol_chiki; X_old_italic; X_old_persian; X_old_south_arabian; X_old_turkic; X_oriya; X_osmanya; X_pig_latin; X_phags_pa; X_phoenician; X_rejang; X_runic; X_samaritan; X_saurashtra; X_sharada; X_shavian; X_sinhala; X_sora_sompeng; X_sundanese; X_syloti_nagri; X_syriac; X_tagalog; X_tagbanwa; X_tai_le; X_tai_tham; X_tai_viet; X_takri; X_tamil; X_telugu; X_thaana; X_thai; X_tibetan; X_tifinagh; X_ugaritic; X_vai; X_yi; Yiddish; Yoruba; Zhuang; Zulu

