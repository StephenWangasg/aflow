#!/bin/bash

#sudo ./start_mongodb.sh

#check if mongodb is install?
if type mongod 2>/dev/null; then
    echo 'mongodb installed'
else
    echo 'mongodb not installed'
    apt-get install mongodb -y
fi

test_path=`dirname $0`
data_path=$test_path/data
mongo_db=$data_path/.mongo

[ -d $mongo_db ] || mkdir -p $mongo_db

mongod --dbpath $mongo_db --noauth

python -m pip install pymongo