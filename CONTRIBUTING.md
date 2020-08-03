# Contributing

Pull requests are welcomed. It is worthwhile opening an issue first to discuss any larger changes to make sure they fit with the project.


## Installing development version

If you wish to install the latest (non-stable) development version from source, download the latest version of the code, either from <http://github.com/dbr/tvnamer/tarball/master> or by running:

    git clone git://github.com/dbr/tvnamer.git

..then `cd` into the directory, and run:

    python setup.py install

You may wish to do this via virtualenv to avoid cluttering your global install

Example terminal session:

    $ virtualenv tvn-env
    [...]
    Installing setuptools, pip, wheel...done.
    $ source tvn-env/bin/activate
    (tvn-env) $ git clone git://github.com/dbr/tvnamer.git
    Cloning into 'tvnamer'...
    [...]
    (tvn-env) $ cd tvnamer/
    (tvn-env) $ python setup.py develop
    [...]
    (tvn-env) $ tvnamer --help
    [...]
    (tvn-env) $ deactivate
    $ tvnamer
    -bash: tvnamer: command not found


## Development setup

First set up a virtual environment (e.g using `mkvirtualenv tvn` then `workon tvn` if you are using [`virtualenvwrapper`](https://pypi.org/project/virtualenvwrapper/))

In this env, install the development tools:

    pip install -r requirements-dev.txt

This installs things like pytest and the coverage module.

Then to execute the test-suite just run

    pytest

This outputs the results of the test-run and a summary of test coverage. To generate the full coverage report run:

    coverage html

Then look at `htmlcov/index.html` in a browser.
