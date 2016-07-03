
Tokenization
============

Tokenization is the process that identifies the text boundaries of words
and sentences. We can identify the boundaries of sentences first then
tokenize each sentence to identify the words that compose the sentence.
Of course, we can do word tokenization first and then segment the token
sequence into sentneces. Tokenization in polyglot relies on the `Unicode
Text Segmentation <http://www.unicode.org/reports/tr29/>`__ algorithm as
implemented by the `ICU Project <http://site.icu-project.org/>`__.

You can use C/C++ ICU library by installing the required package
``libicu-dev``. For example, on ubuntu/debian systems you should use
``apt-get`` utility as the following:

.. code:: python

    sudo apt-get install libicu-dev

.. code:: python

    from polyglot.text import Text

Word Tokenization
-----------------

To call our word tokenizer, first we need to construct a Text object.

.. code:: python

    blob = u"""
    两个月前遭受恐怖袭击的法国巴黎的犹太超市在装修之后周日重新开放，法国内政部长以及超市的管理者都表示，这显示了生命力要比野蛮行为更强大。
    该超市1月9日遭受枪手袭击，导致4人死亡，据悉这起事件与法国《查理周刊》杂志社恐怖袭击案有关。
    """
    text = Text(blob)

The property words will call the word tokenizer.

.. code:: python

    text.words




.. parsed-literal::

    WordList(['两', '个', '月', '前', '遭受', '恐怖', '袭击', '的', '法国', '巴黎', '的', '犹太', '超市', '在', '装修', '之后', '周日', '重新', '开放', '，', '法国', '内政', '部长', '以及', '超市', '的', '管理者', '都', '表示', '，', '这', '显示', '了', '生命力', '要', '比', '野蛮', '行为', '更', '强大', '。', '该', '超市', '1', '月', '9', '日', '遭受', '枪手', '袭击', '，', '导致', '4', '人', '死亡', '，', '据悉', '这', '起', '事件', '与', '法国', '《', '查理', '周刊', '》', '杂志', '社', '恐怖', '袭击', '案', '有关', '。'])



Since ICU boundary break algorithms are language aware, polyglot will
detect the language used first before calling the tokenizer

.. code:: python

    print(text.language)


.. parsed-literal::

    name:             code: zh       confidence:  99.0 read bytes:  1920


Sentence Segementation
----------------------

If we are interested in segmenting the text first into sentences, we can
query the ``sentences`` property

.. code:: python

    text.sentences




.. parsed-literal::

    [Sentence("两个月前遭受恐怖袭击的法国巴黎的犹太超市在装修之后周日重新开放，法国内政部长以及超市的管理者都表示，这显示了生命力要比野蛮行为更强大。"),
     Sentence("该超市1月9日遭受枪手袭击，导致4人死亡，据悉这起事件与法国《查理周刊》杂志社恐怖袭击案有关。")]



``Sentence`` class inherits ``Text``, therefore, we can tokenize each
sentence into words using the same property ``words``

.. code:: python

    first_sentence = text.sentences[0]
    first_sentence.words




.. parsed-literal::

    WordList(['两', '个', '月', '前', '遭受', '恐怖', '袭击', '的', '法国', '巴黎', '的', '犹太', '超市', '在', '装修', '之后', '周日', '重新', '开放', '，', '法国', '内政', '部长', '以及', '超市', '的', '管理者', '都', '表示', '，', '这', '显示', '了', '生命力', '要', '比', '野蛮', '行为', '更', '强大', '。'])



Command Line
------------

The subcommand tokenize does by default sentence segmentation and word
tokenization.

.. code:: python

    ! polyglot tokenize --help


.. parsed-literal::

    usage: polyglot tokenize [-h] [--only-sent | --only-word] [--input [INPUT [INPUT ...]]]
    
    optional arguments:
      -h, --help            show this help message and exit
      --only-sent           Segment sentences without word tokenization
      --only-word           Tokenize words without sentence segmentation
      --input [INPUT [INPUT ...]]


Each line represents a sentence where the words are split by spaces.

.. code:: python

    !polyglot --lang en tokenize --input testdata/cricket.txt


.. parsed-literal::

    Australia posted a World Cup record total of 417 - 6 as they beat Afghanistan by 275 runs .
    David Warner hit 178 off 133 balls , Steve Smith scored 95 while Glenn Maxwell struck 88 in 39 deliveries in the Pool A encounter in Perth .
    Afghanistan were then dismissed for 142 , with Mitchell Johnson and Mitchell Starc taking six wickets between them .
    Australia's score surpassed the 413 - 5 India made against Bermuda in 2007 .
    It continues the pattern of bat dominating ball in this tournament as the third 400 plus score achieved in the pool stages , following South Africa's 408 - 5 and 411 - 4 against West Indies and Ireland respectively .
    The winning margin beats the 257 - run amount by which India beat Bermuda in Port of Spain in 2007 , which was equalled five days ago by South Africa in their victory over West Indies in Sydney .


References
~~~~~~~~~~

-  `Unicode Text Segmentation
   Algorithm <http://www.unicode.org/reports/tr29/>`__
-  `Unicode Line Breaking
   Algorithm <http://www.unicode.org/reports/tr14/>`__
-  `Boundary
   Analysis <http://userguide.icu-project.org/boundaryanalysis>`__
-  `ICU Homepage <http://site.icu-project.org/>`__
-  `Python Wrapper for libicu <https://pypi.python.org/pypi/PyICU>`__
