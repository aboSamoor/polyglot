
Command Line Interface
======================

polyglot package offer a command line interface along with the library
access. For each task in polyglot, there is a subcommand with specific
options for that task. Common options are gathered under the main
command ``polyglot``

.. code:: python

    !polyglot --help


.. parsed-literal::

    usage: polyglot [-h] [--lang LANG] [--delimiter DELIMITER] [--workers WORKERS] [-l LOG] [--debug]
                    {detect,morph,tokenize,download,count,cat,ner,pos,transliteration,sentiment} ...
    
    optional arguments:
      -h, --help            show this help message and exit
      --lang LANG           Language to be processed
      --delimiter DELIMITER
                            Delimiter that seperates documents, records or even sentences.
      --workers WORKERS     Number of parallel processes.
      -l LOG, --log LOG     log verbosity level
      --debug               drop a debugger if an exception is raised.
    
    tools:
      multilingual tools for all languages
    
      {detect,morph,tokenize,download,count,cat,ner,pos,transliteration,sentiment}
        detect              Detect the language(s) used in text.
        tokenize            Tokenize text into sentences and words.
        download            Download polyglot resources and models.
        count               Count words frequency in a corpus.
        cat                 Print the contents of the input file to the screen.
        ner                 Named entity recognition chunking.
        pos                 Part of Speech tagger.
        transliteration     Rewriting the input in the target language script.
        sentiment           Classify text to positive and negative polarity.


Notice that most of the operations are language specific. For example,
tokenization rules and part of speech taggers differ between languages.
Therefore, it is important that the lanaguage of the input is detected
or given. The ``--lang`` option allows you to tell polyglot which
language the input is written in.

.. code:: python

    !polyglot --lang en tokenize --input testdata/cricket.txt | head -n 3


.. parsed-literal::

    Australia posted a World Cup record total of 417 - 6 as they beat Afghanistan by 275 runs .
    David Warner hit 178 off 133 balls , Steve Smith scored 95 while Glenn Maxwell struck 88 in 39 deliveries in the Pool A encounter in Perth .
    Afghanistan were then dismissed for 142 , with Mitchell Johnson and Mitchell Starc taking six wickets between them .


In case the user did not supply the the language code, polyglot will
peek ahead and read the first 1KB of data to detect the language used in
the input.

.. code:: python

    !polyglot tokenize --input testdata/cricket.txt | head -n 3


.. parsed-literal::

    2015-03-15 17:06:45 INFO __main__.py: 276 Language English is detected while reading the first 1128 bytes.
    Australia posted a World Cup record total of 417 - 6 as they beat Afghanistan by 275 runs .
    David Warner hit 178 off 133 balls , Steve Smith scored 95 while Glenn Maxwell struck 88 in 39 deliveries in the Pool A encounter in Perth .
    Afghanistan were then dismissed for 142 , with Mitchell Johnson and Mitchell Starc taking six wickets between them .


Input formats
-------------

Polyglot will process the input contents line by line assuming that the
lines are separated by "``\n``". If the file is formatted differently,
you can use the polyglot main command option ``delimiter`` to specify
any string other than "``\n``".

You can pass text to the polyglot subcommands in several ways:

-  **Standard input**: This is, usually, useful for building processing
   pipelines.

-  **Text file**: The file contents will be processed line by line.

-  **Collection of text files**: Polyglot will iterate over the files
   one by one. If the polyglot main command option ``workers`` is
   activated, the execution will be parallelized and each file will be
   processed by a different process.

Word Count Example
------------------

This example will demonstrate how to use the polyglot main command
options and the subcommand count to generate a count of the words
appearing in a collection of text files.

First, let us examine the subcommand ``count`` options

.. code:: python

    !polyglot count --help


.. parsed-literal::

    usage: polyglot count [-h] [--min-count MIN_COUNT | --most-freq MOST_FREQ] [--input [INPUT [INPUT ...]]]
    
    optional arguments:
      -h, --help            show this help message and exit
      --min-count MIN_COUNT
                            Ignore all words that appear <= min_freq.
      --most-freq MOST_FREQ
                            Consider only the most frequent k words.
      --input [INPUT [INPUT ...]]


To avoid long output, we will restrict the count to the words that
appeared at least twice

.. code:: python

    !polyglot count --input testdata/cricket.txt --min-count 2


.. parsed-literal::

    in	10
    the	6
    by	3
    and	3
    of	3
    Bermuda	2
    West	2
    Mitchell	2
    South	2
    Indies	2
    against	2
    beat	2
    as	2
    India	2
    which	2
    score	2
    Afghanistan	2


Let us consider the scenario where we have hundreds of files that
contains words we want to count. Notice, that we can parallelize the
process by passing a number higher than 1 to the polyglot main command
option ``workers``.

.. code:: python

    !polyglot --log debug --workers 5 count --input testdata/cricket.txt testdata/cricket.txt --min-count 3


.. parsed-literal::

    in	20
    the	12
    of	6
    by	6
    and	6
    West	4
    Afghanistan	4
    India	4
    beat	4
    which	4
    Indies	4
    Bermuda	4
    as	4
    South	4
    Mitchell	4
    against	4
    score	4


Building Pipelines
------------------

The previous subcommand ``count`` assumed that the words are separted by
spaces. Given that we never tokenized the text file, that may result in
suboptimal word counting. Let us take a closer look at the tail of the
word counts

.. code:: python

    !polyglot count --input testdata/cricket.txt | tail -n 10


.. parsed-literal::

    Ireland	1
    surpassed	1
    amount	1
    equalled	1
    a	1
    The	1
    413-5	1
    Africa's	1
    tournament	1
    Johnson	1


Observe that words like "2007." could have been considered two words
"2007" and "." and the same for "Africa's". To fix this issue, we can
use the polyglot subcommand tokenize to deal with these cases. We can
stage the counting to happen after the tokenization using the stdin to
build a simple pipe.

.. code:: python

    !polyglot --lang en tokenize --input testdata/cricket.txt | polyglot count --min-count 2


.. parsed-literal::

    in	10
    the	6
    .	6
    -	5
    ,	4
    of	3
    and	3
    by	3
    South	2
    5	2
    2007	2
    Bermuda	2
    which	2
    score	2
    against	2
    Mitchell	2
    as	2
    West	2
    India	2
    beat	2
    Afghanistan	2
    Indies	2


Notice, that the word "2007" started appearing in the words counts list.
