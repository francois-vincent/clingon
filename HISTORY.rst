.. :changelog:

History
-------

0.3.1 (2020-12-14)
---------------------

* Quickfix of DEBUG mode: now works on python 3


0.3.0 (2016-08-26)
---------------------

* small functional change:
  There is no more options default values from environment variables and configuration files.
  Options default values are set once and only once into the decorated function definition.
  Instead, options runtime values are set from environment variables, configuration files and cli,
  in this order of priority (env vars have least priority, cli has highest).


0.2.0 (2016-07-20)
---------------------

* new feature: allow overloading of default values from configuration file (python, yaml, json)
* code refactor and additional comments
* added french and spanish defaults in user input utility class


0.1.4 (2015-04-23)
---------------------

* can override default options from environ, via variable CLINGON_PREFIX (see example2)
* utility class for user input management, with unittests
* updated README
* fix debug output 'clize default parameters'
* some code refactoring


0.1.3 (2015-03-27)
---------------------

* fix list option when default is empty
* default value of boolean must be False
* if list option is given with non empty default, check number of arguments
* new example


0.1.2 (2015-02-25)
---------------------

* setup.py now installs clingon command,
* so, option auto_install as been removed
* refactor error handling in script. There's an exception RunnerErrorWithUsage
  that prints single line usage string before error messsage
* better handle of duplicate short aliases


0.1.1 (2015-02-24)
---------------------

* update print_version()
* allow clingon to autoinstall in a more simpler way
* some minor fixes
* some more unittests


0.1.0 (2015-02-23)
---------------------

* First release on PyPI.
