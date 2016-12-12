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

############### airflow ####################
if you see errors such as 'failed to connect to cluster...', try clear system cache first before starting airflow server:
echo 3 > /proc/sys/vm/drop_caches

############ run services #############################
1. start airflow server
 airflow webserver -hn 0.0.0.0 -p 8080
2. start airflow
 airflow scheduler
3. feature.py
 cd ../flow
 PYTHONPATH=.. python feature.py
4. nginx and uwsgi
# For the 1st time you run uwsgi on a machine
# step 1. create a master fifo file
vim /tmp/uwsgi_fifo
# Step 2. start the uwsgi in chain reloading mode for gracefull reloading
uwsgi --ini webapp_uwsgi.ini --lazy-apps --master-fifo /tmp/uwsgi_fifo
# Next time when you want to restart uwsgi for code updates or bug fixes:
echo c > /tmp/uwsgi_fifo
# To kill existing uwsgi processes (if necessary):
#show uwsgi processes
ps -eaf | grep uwsgi
#kill uwsgi
kill -9 [process number]
