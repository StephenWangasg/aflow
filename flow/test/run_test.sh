#!/bin/bash

#simply run run_test.sh to run all tests
#`run_test.sh -h` to get help message

pushd `dirname $0` > /dev/null

test_path=`pwd -P`
flow_path=`dirname $test_path`
root_path=`dirname $flow_path`

#add flow path to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$root_path

python main.py "$@"

popd > /dev/null