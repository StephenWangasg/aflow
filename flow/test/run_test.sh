#!/bin/bash

#***********************************************************
#| HAVE PATIENCE WITH THIS MINUTES LONG TEST! FOR LAO TZU, |
#| IT WAS ONE OF THE THREE GREATEST TREASURES TO HAVE,     |
#| ALONG WITH COMPASSION AND SIMPLICITY.                   |
#***********************************************************

#simply run run_test.sh to run all tests
#Test framework: pytest
#To install:
#sudo pip install -U pytest

#check if pytest is installed
pytest --version > /dev/null 2>&1 || { echo "pytest is not installed, to install, run: 'pip install -U pytest'" && exit 1; }

pushd `dirname $0` > /dev/null

test_path=`pwd -P`
flow_path=`dirname $test_path`
root_path=`dirname $flow_path`
temp_path=$flow_path/test/.temp

rm -rf $temp_path

#add flow path to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$root_path

python -m pytest --basetemp=$temp_path $test_path

popd > /dev/null