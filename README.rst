Tests for `MI-PYT <https://github.com/cvut/MI-PYT>`__ Labelord homework
=======================================================================

Usage
-----

 1. Copy the tests files to your project.
 2. Use the skeleton of ``labelord.py`` for implementation (see notes).
 3. In your virtual environment, install pytest: ``python -m pip install click requests betamax flexmock pytest flask``.
 4. Run ``python -m pytest tests_cli/`` to run tests for CLI app (from previous task).
 4. Run ``python -m pytest tests_web/`` to run tests for WEB app.


Notes and hints
---------------

* You need to pass the context to click in same manner as in skeleton because it is being used in tests for injecting resources to  your implementation.
* You need to request repositories and labels with page size set explicitly to 100 and then paging (even if you need page 1) ->  ``?per_page=100&page=1``
* Tests use spy on session to check correct count of requests per type. Sometimes it can shadow real problem and you will see something like ``flexmock.MethodCallError: get() expected to be called exactly 2 times, called 0 times`` instead of failing assertion or thrown exception. To disable this checks you need to set environment variable ``LABELORD_SESSION_SPY`` to value ``off``. Example for Linux:

::

   $ export LABELORD_SESSION_SPY=off
   $ python -m pytest pytest tests_web/
   $ unset LABELORD_SESSION_SPY
   $ python -m pytest pytest tests_web/

* For easier work, you can use various pytest options (see `documentation <https://docs.pytest.org/en/latest/usage.html>`__), for example:

  * ``--maxfail`` - to set number fails until it stops testing
  * ``-k`` - keyword expression for filtering tests
  * ``tests/test_file.py::test_func`` - give exact file as an arguments (or fully qualified test name)

* Methods ``inject_session`` and ``reload_config`` of ``LabelordWeb`` are used by tests to provide special session for testing the communication with GitHub just as in previous task via click context. If ``inject_session`` is not called, create own new session. In the new click subcommand ``run_server`` pass the session from context (as in other subcommands) to the web app.

* You should be able to use the CLI application. Your web application should not cause an error (exit with exit code > 0 and error message) unless is being used and badly configured.

Frequent errors
----------------

Error with bad request
***********************

::

 <Result BetamaxError("A request was made that could not be handled.
 A request was made to https://api.github.com/*****
 The settings on the cassette are -
   record_mode: none
   match_options {'uri', 'method'}.\n",)>.exit_code


That happen if you do some requests, that tests don't expect. You can find list of allowed request urls in ``tests/fixtures/casettes/*``


Betamax Error: object has no attribute 'message'
************************************************

::

<[AttributeError("'BetamaxError' object has no attribute 'message'") raised in repr()] Result object at 0x7f74dbc864e0>.exit_code


This is error in Betamax library. You must edit Betamax Exception. Edit in (virtual environment): ``__venv__/lib/python*.*/site-packages/betamax/exceptions.py`` and delete lines:

::

 def __repr__(self):
     return 'BetamaxError("%s")' % self.message


Betamax Error: A request was made that could not be handled
***********************************************************

The tests are written in a way that thay anticipate a series of HTTP requests happening during a test. Any extra requests are "forbidden". The motivation for this is not you to have tied hands, this is happening because all HTTP coomunication is faked in the tests. When in doubt, inspect the appropriate json file in ``tests/fixtures/cassettes``.


License
-------

This code has been dedicated to the Public Domain, it is licensed with
`CC0 1.0 Universal Public Domain
Dedication <https://creativecommons.org/publicdomain/zero/1.0/>`__,
full text of the license is available in the LICENSE file in this
repository.
