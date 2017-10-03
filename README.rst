Tests for `MI-PYT <https://github.com/cvut/MI-PYT>`__ Labelord homework
=======================================================================

Usage
-----

 1. Copy the tests files to your project.
 2. Use the skeleton of ``labelord.py`` for implementation (see notes).
 3. In your virtual environment, install pytest: ``python -m pip install click requests betamax flexmock pytest``.
 4. Run ``python -m pytest tests/``.


Notes:

* You need to pass the context to click in same manner as in skeleton because it is being used in tests for injecting resources to  your implementation.
* You need to request repositories and labels with page size set explicitly to 100 and then paging (even if you need page 1) ->  ``?per_page=100&page=1``
* Tests use spy on session to check correct count of requests per type. Sometimes it can shadow real problem and you will see something like ``flexmock.MethodCallError: get() expected to be called exactly 2 times, called 0 times`` instead of failing assertion or thrown exception. To disable this checks you need to set environment variable ``LABELORD_SESSION_SPY`` to value ``off``. Example for Linux:

::

   $ export LABELORD_SESSION_SPY=off
   $ python -m pytest pytest tests/
   $ unset LABELORD_SESSION_SPY
   $ python -m pytest pytest tests/


License
-------

This code has been dedicated to the Public Domain, it is licensed with
`CC0 1.0 Universal Public Domain
Dedication <https://creativecommons.org/publicdomain/zero/1.0/>`__,
full text of the license is available in the LICENSE file in this
repository.
