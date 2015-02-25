.. :changelog:

History
-------

0.1.0 (2015-02-23)
---------------------

* First release on PyPI.


0.1.1 (2015-02-24)
---------------------

* update print_version()
* allow clingon to autoinstall in a more simpler way
* some minor fixes
³ some more unittests


0.1.2 (2015-02-25)
---------------------

* setup.py now installs clingon command,
* so, option auto_install as been removed
* refactor error handling in script. There's an exception RunnerErrorWithUsage
  that prints single line usage string before error messsage
* better handle duplicate short aliases
