.. :changelog:

History
-------


0.1.4 (TBD)
---------------------

* some code refactoring
* a better README
* optionally can override default options from environ


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
