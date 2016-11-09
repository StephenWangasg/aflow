# install mongo https://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/
export LC_ALL=C
sudo pip install pymongo

# install PIL
sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
sudo pip install Pillow

# install boto
pip install boto
