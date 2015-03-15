
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

Monolingual Text
~~~~~~~~~~~~~~~~

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
~~~~~~~~~~

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
    
    


Tricky cases
~~~~~~~~~~~~

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

    <ipython-input-13-de43776398b9> in <module>()
    ----> 1 print(Detector("4"))
    

    /usr/local/lib/python2.7/dist-packages/polyglot-15.03.12-py2.7.egg/polyglot/detect/base.pyc in __init__(self, text, quiet)
         63     self.quiet = quiet
         64     """If true, exceptions will be silenced."""
    ---> 65     self.detect(text)
         66 
         67   def detect(self, text, quiet=False):


    /usr/local/lib/python2.7/dist-packages/polyglot-15.03.12-py2.7.egg/polyglot/detect/base.pyc in detect(self, text, quiet)
         84 
         85       if not reliable and not self.quiet:
    ---> 86         raise UnknownLanguage("Try passing a longer snippet of text")
         87       else:
         88         logger.warning("Detector is not able to detect the language reliably.")


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

