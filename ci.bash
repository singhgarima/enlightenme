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
    echo "Running the tests"
    pipenv run coverage run setup.py test
    pipenv run coverage report
}

function main () {
    lint || return 1
    build || return 1
    run-test || return 1
}

main "$@" || exit 1
exit 0