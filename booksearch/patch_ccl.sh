#!/bin/sh
basepath=`find ./usr/ -name 'PyZ3950'`
ccl=`find $basepath -name ccl.py`
echo "Patching $ccl"
sed -i -e 's/^import lex$/from ply import lex/' $ccl
sed -i -e 's/^import yacc$/from ply import yacc/' $ccl
