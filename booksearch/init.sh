#!/usr/bin/env bash

# Install script for BookSearch,
# Checks basic requirement needed to run.
#
# Author: Willem Jan Faber
# Licence: MIT
#

function help {
    echo -e "Please run the following command:\n\n"
    echo -e "sudo apt-get install build-essential libxml2-dev libxslt1-dev python-dev python-pip realpath python-virtualenv\n"
    exit -1
}

function check_package () {
    # Checking if given file is in the system path,
    # else presume that a package is missing.

    echo "Checking for $1"

    package=`which $1`

    if [ -z $package ]
    then
        echo "$1 not found.."
        help
    else
        echo -e "$1 installed ($package)..\n"
    fi
}

function check_requirements {
    check_package make
    check_package virtualenv
    check_package pip
    check_package realpath
    check_package python-config
    check_package xslt-config
    check_package xml2-config
}

echo -e "\n"
check_requirements

script_path=`realpath $0`
cd `dirname "$script_path"`

# Install tools
echo -e "\nSetting up virtualenv.."
virtualenv env
source env/bin/activate

echo "All init requirements ok."
