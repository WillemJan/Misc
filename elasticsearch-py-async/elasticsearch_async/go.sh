#!/bin/bash

check_for_deps(){
    type -P a2ps &>/dev/null || { echo "a2ps was not found.  Install package \"a2ps\" on Debian or equivalent."; exit 1; }
    type -P ps2pdf &>/dev/null || { echo "a2ps was not found.  Install package \"ghostscript\" on Debian or equivalent."; exit 1; }
}

check_exists(){
    if [ ! -f $1 ]; then
            echo "File \"$1\" is missing."
            exit 1
    fi
}

gen_source(){
    check_exists $1
    echo "Generating code.pdf..."
    rm -f code.ps code.pdf
        a2ps -1 -E --pro=color --right-title="" -q -b"" -o code.ps $1
        ps2pdf code.ps
        rm code.ps
}

gen_log(){
    check_exists $1
    echo "Generating log.pdf..."
    rm -f log.ps log.pdf
        a2ps -1 --center-title="Console Log" -q -b"" -o log.ps $1
        ps2pdf log.ps
        rm log.ps

}

check_for_deps

if [ $# -ne 2 ]; then
        echo "This tool will take a source code file and console log and generate prettyprinted PDFs."
        echo "Usage:    `basename $0` {source-file} {console-log-file}"
        echo "          `basename $0` --just-source {source-file}"
        echo "          `basename $0` --just-console {console-log-file}"
        echo "Author: Joshua Steiner (http://jbsteiner.com)"
        exit 1
else
        if [ "$1" == "--just-source" ]; then
              gen_source $2
        elif [ "$1" == "--just-console" ]; then
              gen_log $2
        else
              gen_source $1
              gen_log $2
        fi
fi

echo "Files were successfully generated in directory \"`pwd`\"."

