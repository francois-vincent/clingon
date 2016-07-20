===========================================================
**clingon** - Command Line INterpreter Generator for pythON
===========================================================

.. image:: https://travis-ci.org/francois-vincent/clingon.png?branch=master
   :target: https://travis-ci.org/francois-vincent/clingon

.. image:: https://codecov.io/github/francois-vincent/clingon/coverage.svg?branch=master
   :target: https://codecov.io/github/francois-vincent/clingon

.. image:: https://pypip.in/version/clingon/badge.svg
   :target: https://pypi.python.org/pypi/clingon

.. image:: https://pypip.in/py_versions/clingon/badge.svg
   :target: https://pypi.python.org/pypi/clingon/

.. image:: https://pypip.in/download/clingon/badge.svg
   :target: https://pypi.python.org/pypi/clingon/


A super handy command line interpreter generator
------------------------------------------------

.. figure:: http://www.ex-astris-scientia.org/inconsistencies/klingons/klingon-gorkon-theundiscoveredcountry.jpg
   :alt: clingon

Clingon is the conjunction of a function decorator and a command line tool
that gives you the super power to create shell scripts in a snap.

The function decorator converts a python function into a command line script
and the command line tool can install this script where you want, ready for
execution. You have created a new command line tool in minutes !

A help output is also automatically created from your function docstring and
signature, with types and default values.

No dependency, except some standard modules (and orderddict for py26).
Works under python 2 and 3.
Tested for Cpython 2.6, 2.7, 3.3, 3.4, and Pypy.
Runs under linux (OSX under construction).

Installation
~~~~~~~~~~~~

.. code:: sh

    $ pip install clingon

This will install clingon as a module (providing the decorator) as well as a script
(providing the script installer).

How to use
~~~~~~~~~~

That's dead simple, just prepend the decorator to your function and it
is converted to a command line script. Then you can run the installer on your
new script if you want.

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

Corresponding usage examples (without installer):

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

You just have to follow some simple rules when defining your
parameters:

Required parameters are defined first, as basic positional python parameters
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
a ``sys.exit(1)``. You can override this and see the original
exception with call stack by setting clingon.DEBUG = True immediately after
the import.

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

- A usage string, i.e. script name and parameters,
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

- Any missing required parameter,
- Unrecognized parameter or option,
- Duplicate option,
- Missing value of option,
- Type of option if numerical option (also for lists of numbers),
- Number of elements in list option must match that of default if default is non empty.

There's more
~~~~~~~~~~~~

Two convenience exceptions are available for you to use in your script:
``RunnerError`` prompts the given message to stderr, and then sys.exit(1).
``RunnerErrorWithUsage`` prepends a usage string before your error message
in stderr, and then sys.exit(1).

You can specify a variable list of parameters by adding a ``*args``
parameter to your python function, with the usual constraint that it
must be the last one. This construct allows you to partially control the
number of parameters your function accepts. You can specify a lower
limit by specifying some required parameters, but if you want to specify
an upper limit, you have to code it explicitly into your function.

Additionally, you can specify some variables that can be used inside the decorated
function docstring (with usual python format() mustache notation). This allows
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

Specifying a ``VERSION`` variable will also automatically add a version option
``(--version \| -V)``.

There is another special variable ``CLINGON_PREFIX`` that allows you to specify
an environment variable prefix for all your default options, giving you the possibility
to override default options (see example2.py).
For example, specifying ``@clingon.set_variables(CLINGON_PREFIX="MY_SCRIPT")`` in the
example above, then having some ``export MY_SCRIPT_FIRST_OPTION="another_default_value"``
in your environment will override ``first_option`` default value to "another_default_value".

Another default value override mechanism is provided through configuration files.
For example, adding decorator ``@clingon.set_variables(DEFAULTS_FILE='defaults.yml')`` will search
and read a configuration file specifing overrides for defaults values.
Supported configuration formats are python, yaml and json. See example5.py and docstring of method
``override_defaults_from_file`` for more details on this feature.

Command line script installer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The clingon script can also turn your brand new python script into a new
command available locally or globally. Just run the clingon tool on
your script, with relevant options: zero option will copy clingon in the
same path as the python executable (will be the current python venv if activated),
--user will copy it to your ~/bin folder, and --target-path to the specified path.

.. code:: sh

    clingon python_script [options] [--help | -?]

    Options:
    --target-path      | -p <str> (default='')
    --target-name      | -n <str> (default='')
    --user             | -u (default=False)
    --make-link        | -m | -s | -l (default=False)
    --force            | -f | -o (default=False)
    --remove           | -r (default=False)
    --no-check-shebang (default=False)
    --no-check-path    (default=False)
    --version          | -V print version (0.1.2)
    --help             | -? print this help


Utilities
~~~~~~~~~

There is a utility module containing a user input management class named AreYouSure.
This class implements a highly customizable binary (True or False) oracle with the capacity
to lock its state to be always True or always False.

Typical usage (see example4.py):

.. code:: python

    # file script.py
    from clingon import clingon
    from clingon.utils import AreYouSure
    import os.path

    @clingon.clize
    def copy(source, force=False, *dest):
        ays = AreYouSure(output='stderr')
        for d in dest:
            if os.path.exists(d) and (force or ays('%s already exists, replace it' % d)):
                print("replacing %s" % d)
                ....


This will result in user input prompt:

.. code:: sh

    dest already exists, replace it [yes,y,no(default),ALL,NONE] ?

Typing 'y' or 'yes' on an item will print ``replacing dest`` for this item, typing 'no' or
just hitting enter key will skip the item. Typing 'ALL' will skip prompt but perform print
for each item, and typing 'NONE' will skip all prompts and prints.
The prompt message, its destination (stdout or stderr), all the expected inputs, default when
hitting enter key, and case considerations are customizable.


Licence
~~~~~~~

BSD license


See also
~~~~~~~~

clint [https://pypi.python.org/pypi/clint/]
comes with excellent support for colors, indentation, multi-columns and progress-bar


Cheers
~~~~~~~

CookieCutter [https://github.com/audreyr/cookiecutter]
especially the Python section.


Author
~~~~~~

François Vincent [https://github.com/francois-vincent]
