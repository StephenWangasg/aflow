from cv.config import *
from cv.retrieval.create_db import create_aero_master
from cv.retrieval.annoy_index import build_annoy_index, build_annoy_index_all_filter

from ingest.schedule import DayScheduler
from cv.retrieval.matcher_2 import Server
import subprocess

# regenerate areospike database, annoy indexes and reload server daily at a certain time in hour
def reload_server(hour = 4):
    ds = DayScheduler(hour)
    for d in ds.is_time_to_run():
        st = '/set'
        s = Server(query_server['host'], query_server['port'])
        set_name = s.return_response(st)

        # check if create on a different set or current
        set_name_2 = 'two' if set_name == 'one' else 'one'

        create_aero_master(set_name_2)
        build_annoy_index(set_name_2)
        build_annoy_index_all_filter(set_name_2)

        # chain reloading workers processes:
        subprocess.call(['echo c > /tmp/uwsgi_fifo'])

        # for chain reloading: the uwsgi server should be started by:
        # uwsgi --reload /var/tmp/uwsgi.pid --lazy-apps --master-fifo /tmp/uwsgi_fifo
        ## --touch-chain-reload may also be used
