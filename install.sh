# install mongo https://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/
export LC_ALL=C
sudo pip install pymongo

############# for image resizing and pushing to S3
# install PIL
sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
sudo pip install Pillow
# install boto
pip install boto

############ run services #############################
1. start airflow server
 airflow webserver -hn 0.0.0.0 -p 8080
2. start airflow
 airflow scheduler
3. feature.py
 cd ../flow
 PYTHONPATH=.. python feature.py
