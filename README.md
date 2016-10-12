# NuPIC Regression Tests

The tests in this repository are [regression tests](http://en.wikipedia.org/wiki/Regression_testing). These tests are meant to maintain a standard of performance by running longer functional tests for NuPIC after every successful build of the [nupic](https://github.com/numenta/nupic) `master` branch in Travis-CI.

## WARNING

**DO NOT EDIT THE `nupic_sha.txt` FILE!**

This file is automatically updated by the tooling server, and should never be manually edited.

## What kind of tests to write

The tests in this repository are Python [unittest2](https://pypi.python.org/pypi/unittest2) tests (but they are **not** unit tests). These tests should not test units of code, but the system as a whole. For example, one test might be to feed in a certain set of input data and assert that 5-step ahead predictions are within a defined range of error after 1000 rows of data.

## How to add tests

Each test should describe exactly what it is testing in a docstring, and extent the `TestCase` class for automatic inclusion in the test suite. Please see example test(s) in the `tests` directory for details.

## Running regression tests locally

To run locally against the target SHA (see `nupic_sha.txt`), be sure you've installed NuPIC properly at the specified SHA.

    export REGRESSION_SHA_TARGET=`cat nupic_sha.txt`
    # Go into NuPIC and install at target SHA
    pushd $NUPIC
    git pull upstream master
    git checkout ${REGRESSION_SHA_TARGET}
    git clean -dfx # careful here, you might nuke something you don't want to nuke
    python setup.py install --user
    popd
    # Back to regression folder to run tests
    py.test tests/

Included in `tests/anomaly/` is a regression test for [NAB](https://github.com/numenta/NAB). To run locally you must have a NAB environment variable setup that points to your NAB clone repositiory:

	export NAB='path/to/NAB/'
	py.test tests/anomaly/nab/ # run NAB regression test

### Dependencies for running locally

    pip install requests
    pip install automatatron

## How it works

On every build of the [nupic](https://github.com/numenta/nupic) `master` branch in Travis-CI, an archive of the `release` folder (including pip requirements) is uploaded to Amazon S3 for the latest commit SHA. When the `nupic` build completes, the [tooling server](https://github.com/numenta/nupic.tools) updates the SHA stored in `nupic_sha.txt` to the latest SHA that ran in Travis-CI and pushes it to `nupic.regression`.`master`. This triggers a regression test run in Travis-CI.

When `nupic.regression` runs in Travis-CI, it downloads the archive for the `nupic` SHA specified in `nupic_sha.txt` into a local folder. Because the archive was build in the same Travis-CI environment as `nupic.regression` runs, the installation is compatible. All tests that comply with `unittest2` format in the `tests` directory are run.

