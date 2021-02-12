# Nextstrain CLI Development
<!-- WARNING -->
<!-- Do not edit this file from within the docs.nextstrain.org repository. -->
<!-- It is fetched from another repository to be included in the docs.nextstrain.org build. -->
<!-- So, if you edit it after it is fetched into docs.nextstrain.org, your changes will be lost. -->
<!-- Instead, edit this file in its own repository and commit your changes there. -->
<!-- For more details on this (temporary) implementation, see https://github.com/nextstrain/docs.nextstrain.org#fetching-of-documents-from-other-repositories -->
<!-- This file is fetched from: https://github.com/nextstrain/cli/blob/master/doc/development.md -->
<!-- WARNING -->
<!-- WARNING -->

Development of `nextstrain-cli` happens at <https://github.com/nextstrain/cli>.

We currently target compatibility with Python 3.6 and higher.

Versions for this project follow the [Semantic Versioning rules][].

## Setup

You can use [Pipenv](https://pipenv.pypa.io) to spin up an isolated development
environment:

    pipenv sync --dev
    pipenv run nextstrain --help

The Pipenv development environment includes our dev tools (described below):

    pipenv run pytest           # runs doctests as well as mypy and flake8
    pipenv run mypy nextstrain
    pipenv run flake8

## Running with local changes

From within a clone of the git repository you can run `./bin/nextstrain` to
test your local changes without installing them.  (Note that `./bin/nextstrain`
is not the script that gets installed by pip as `nextstrain`; that script is
generated by the `entry_points` configuration in `setup.py`.)

## Releasing

New releases are made frequently and tagged in git using a [_signed_ tag][].
The source and wheel (binary) distributions are uploaded to [the nextstrain-cli
project on PyPi](https://pypi.org/project/nextstrain-cli).

There is a `./devel/release` script which will prepare a new release from your
local repository.  It ends with instructions for you on how to push the release
commit/tag and how to upload the built distributions to PyPi.  You'll need [a
PyPi account][] and [twine][] installed.

## Tests

Tests are run with [pytest](https://pytest.org).  To run everything, use:

    pytest

This includes the type annotation and static analysis checks described below.

## Type annotations and static analysis

Our goal is to gradually add [type annotations][] to our code so that we can
catch errors earlier and be explicit about the interfaces expected and
provided.  Annotation pairs well with the functional approach taken by the
package.

During development you can run static type checks using [mypy][]:

    $ mypy nextstrain
    # No output is good!

There are also many [editor integrations for mypy][].

The [`typing_extensions`][] module should be used for features added to the
standard `typings` module after 3.6.  (Currently this isn't necessary since we
don't use those features.)

We also use [Flake8][] for some static analysis checks focusing on runtime
safety and correctness.  You can run them like this:

    $ flake8
    # No output is good!


[Semantic Versioning rules]: https://semver.org
[_signed_ tag]: https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work
[a PyPi account]: https://pypi.org/account/register/
[twine]: https://pypi.org/project/twine
[type annotations]: https://www.python.org/dev/peps/pep-0484/
[mypy]: http://mypy-lang.org/
[editor integrations for mypy]: https://github.com/python/mypy#ide--linter-integrations
[`typing_extensions`]: https://pypi.org/project/typing-extensions
[Flake8]: https://flake8.pycqa.org