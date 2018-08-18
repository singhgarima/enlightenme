#!/bin/bash
set -eo pipefail

function lint () {
    echo "Checking the code syntax"
    pipenv run pycodestyle --first enlightenme
}

function build () {
    echo "Building the package"
    pipenv run python setup.py build
}

function run-test () {
    echo "Releasing the pachaage"
    python setup.py release

    echo "Running the tests"
    pipenv run coverage run setup.py test
    pipenv run coverage report
}

function release () {
    echo "Publishing to PyPI"
    pipenv run pip install twine
    pipenv run twine upload dist/* -u ${PYPI_USER_NAME} -p ${PYPI_PWD}
}

function main () {
    lint || return 1
    build || return 1
    run-test || return 1

    echo "VERSION = ${TRAVIS_PYTHON_VERSION}"
    echo "TAG = ${TRAVIS_TAG}"
    if [[ $TRAVIS_PYTHON_VERSION =~ ^3\.6+$ ]]; then
        echo "Version matched for release"
        if [[ $TRAVIS_TAG =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "Releasing tag $TRAVIS_TAG with Python $TRAVIS_PYTHON_VERSION"
            release || return 1
        fi
    fi
}

main "$@" || exit 1
exit 0