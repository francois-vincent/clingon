===========================================================
**clingon** - Command Line INterpreter Generator for pythON
===========================================================

.. image:: https://travis-ci.org/francois-vincent/clingon.png?branch=master
   :target: https://travis-ci.org/francois-vincent/clingon

.. image:: https://codecov.io/github/francois-vincent/clingon/coverage.svg?branch=master
   :target: https://codecov.io/github/francois-vincent/clingon

A handy command line interpreter generator
------------------------------------------

.. figure:: http://www.ex-astris-scientia.org/inconsistencies/klingons/klingon-gorkon-theundiscoveredcountry.jpg
   :alt: clingon

Clingon essentially provides a function decorator that converts a python
function into a command line script in a snap.

The decorator introspects your function signature, then parses the
parameters of your command line. It then calls your function with
parameters checked and instanciated from your command line. A help
output is also automatically created from your function docstring and
parameters, with types and default values.

No dependency, except some standard modules (and orderddict for py26).
Works under python 2 and 3. Tested for Cpython 2.6, 2.7, 3.3, 3.4, and Pypy.

Installation
~~~~~~~~~~~~

.. code:: sh

    $ pip install clingon

How to use
~~~~~~~~~~

That's dead simple, just prepend the decorator to your function and it
is converted to a command line script.

Basic example
^^^^^^^^^^^^^

.. code:: python

    # file script.py
    from clingon import clingon

    @clingon.clize
    def my_script(p1, p2,
                  first_option='default_value',
                  second_option=5,
                  third_option=[4, 3],
                  last_option=False):
        """Write description of your script here.
        """
        # your code

Corresponding usage examples:

.. code:: sh

    $ python script.py toto titi
    $ python script.py toto titi --first-option another_value
    $ python script.py toto titi -f another_value
    $ python script.py toto titi --second-option 10
    $ python script.py toto titi -s 10
    $ python script.py toto titi -t 16 9
    $ python script.py toto titi -l
    $ python script.py toto titi -f another_value -s 10 -t 16 9 -l
    $ python script.py -?

You only have to follow some simple rules when defining your
parameters:

Required parameters are defined as basic positional python parameters
(like the 2 first in the example above). Options are defined as python
keyword parameters, they have default values (like the 4 last parameters
above). As you can see, the Python parameter semantics is easily mapped
onto a sound command line semantics, very close to the Posix standard.
Of course you must respect python variable naming rules. Option names are
lower cased and '\_' are converted to '-', such that a python option 'GLOBAL'
is converted to CLI option '--global' and 'make_link' is converted to
'--make-link'.

You can specify the script system return code by returning an integer
value. Any ``return x`` in the decorated function, with x an integer,
will result into a ``sys.exit(x)``. Any return value other than an int
(including None), will be translated into ``sys.exit(0)``.

If an exception is raised in the decorated function, it will be catched
by the decorator and converted to a one line stderr output, followed by
a ``sys.exit(1)``. You can override this and raise the original
exception by setting clingon.DEBUG = True immediately after the import.

That's it ! Writing python command line scripts had never been that
simple yet !

What is really cool with clingon is that you can change your mind at any
time, changing or adding a parameter is immediate, no need to read
argparse documentation again.

You can specify your short options names as well
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As you can see from the example above, clingon automatically gives short
aliases to options. Default alias consist in the first letter of the
parameter name. Your can override this and define what short parameters
you want (you can specify more than one). All you need is to specify
some keywords to your decorator:

.. code:: python

    # file script2.py
    from clingon import clingon

    @clingon.clize(first_option=('first', 'f'), last_option=('last', 'l'))
    def my_script(p1, p2,
                  first_option='default_value',
                  second_option=5,
                  third_option=[4, 3],
                  last_option=False):
        """Write description of your script here.
        """
        # your code

This is particularly useful when you happen to have options with the
same first letter. In this case, if you do not provide any shortcut,
clingon will silently resolve the conflicting names by allowing one to
have a short alias while the other will have none.

Automatic help
~~~~~~~~~~~~~~

A help is automatically generated, including:

- Usage string, i.e. script name and parameters,
- The docstring of your function, reformated, 
- A detailed description of the options, with names, short names, types and default values.

.. code:: sh

    $ python script2.py -?

      script2.py p1 p2 [options] [--help | -?]

      Write description of your script here.

    Options:
    --first-option  | -first | -f <str> (default='default_value')
    --second-option | -s <int> (default=5)
    --third-option  | -t <list of int> (default=[4, 3])
    --last-option   | -last | -l  (default=False)
    --help          | -? print this help

Checkings
^^^^^^^^^

Options are typed and (basic) type checking is performed by clingon. The
types are automatically derived from the default values. The allowed
types are: ``string``, ``integer``, ``float``, ``boolean`` and
``list of string``, ``list of integer`` and ``list of float``. The
default value of a boolean parameter must always be False.

As you can see in the example above, all options except boolean require
a value. When calling your script, clingon not only checks the types of
your parameters, but also: 

- Any missing required parameters,
- Unrecognized parameter or option,
- Missing value of option,
- Duplicate option.

There's more
~~~~~~~~~~~~

You can specify a variable list of parameters by adding a ``*args``
parameter to your python function, with the usual constraint that it
must be the last one. This construct allows you to partially control the
number of parameters your function accepts. You can specify a lower
limit by specifying some required parameters, but if you want to specify
an upper limit, you have to code it explicitly into your function.

You can specify variables that can be used inside the decorated function
docstring (with usual python format() mustache notation). This allows
you to have a dynamic help description. One useful usage is to include
the version of your script into your help string.

example

.. code:: python

    # file script.py
    from clingon import clingon

    @clingon.clize
    @clingon.set_variables(VERSION=1.2.3)
    def my_script(p1, p2,
                  first_option='default_value',
                  second_option=5,
                  third_option=[4, 3],
                  last_option=False):
        """v{VERSION}
        Write description of your script here.
        """
        # your code

Specifying a VERSION variable will also automatically add a new option
(--version \| -V).

Bonus
~~~~~

As a bonus, clingon can also turn your brand new python script into a
command available locally or globally. Just run the clingon module on
your script, with option --path or --global-script:

.. code::
    python clingon.py path/to/your/script [options]

    Options:
    --target-path      | -p <str> (default='')
    --target-name      | -n <str> (default='')
    --user             | -u (default=False)
    --make-link        | -m | -s | -l (default=False)
    --force            | -f | -o (default=False)
    --remove           | -r (default=False)
    --no-check-shebang | -n (default=False)
    --version          | -V print version
    --help             | -? print this help


This will copy your script to '--path' if specified, or to ~/bin if '--user' is specified or
to your local python path by default, and set the proper execution rights.

Of course, you can clingon clingon itself !

Licence
~~~~~~~

BSD license

Author
~~~~~~

``(c)`` François Vincent [https://github.com/francois-vincent]
