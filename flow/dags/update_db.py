# 'update_db DAG definition'

import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import get_task_id
from flow.configures.conf import CONFIGS, CATEGORIES, WEBSITES, COUNTRIES, LAYER, LAYER_DIMENSION, ATTRIBUTE_LENGTH, ATTRIBUTE_MAP, get_dag_args
from flow.utilities.utils import Server
from flow.utilities.access import Access
import cPickle as pickle
import subprocess
import time
from annoy import AnnoyIndex
import json
import aerospike


# from flow.db_transfer import get_alternate_set, empty_aero_set, create_annoy_for_categories, create_annoy_for_filters, restart_server, mongo2aero
# from flow.dags.utils import updatedb_args

UPDATE_DB_DAG = DAG('update_db', get_dag_args('updatedb'))
client = aerospike.client(CONFIGS['aerospike']).connect()


def _restart_server(_set):
    with open(CONFIGS['model_path'] + "nsfile.txt", "w") as text_file:
        text_file.write(_set)
    subprocess.call(
        "ssh -i /home/ubuntu/iq-vision-dev.pem ubuntu@172.31.2.224 'sudo /home/ubuntu/dev/fashion-query-service/webapp/reload.sh'", shell=True)


def restart_server(**kwargs):
    ti = kwargs['ti']
    _set = ti.xcom_pull(key='set', task_ids='get_alternate_set')
    _restart_server(_set)


def _empty_aero_set(_set):
    for idx in range(100000000):
        key = ('fashion', _set, str(idx))
        try:
            client.remove(key)
        except:
            break


def empty_aero_set(**kwargs):
    ti = kwargs['ti']
    _set = ti.xcom_pull(key='set', task_ids='get_alternate_set')
    _empty_aero_set(_set)


def _mongo2aero(_set):
    product_map = {}
    accessor = Access(CONFIGS)
    for idx, product in enumerate(accessor.products.find({'extracted': True})):
        bins = {k: product[k] for k in product if
                not (('FC7' in k) or ('FC6' in k)
                     or (k in ['discounted_price', 'product_url_hash', '_id']))}
        bins['id'] = idx
        key = ('fashion', _set, str(idx))
        client.put(key, bins)
        product_map[bins['hashedId']] = bins['id']
    with open(CONFIGS['model_path'] + 'annoy_index_files/' + _set + '/' + 'hashedIdmap.p', 'wb') as f:
        pickle.dump(product_map, f)


def mongo2aero(**kwargs):
    ti = kwargs['ti']
    _set = ti.xcom_pull(key='set', task_ids='get_alternate_set')
    _mongo2aero(_set)


def _create_annoy_for_categories(_set):
    import aerospike.predicates as p
    for gender in ['m', 'f']:
        for category in CATEGORIES:
            for location in COUNTRIES:
                query = client.query('fashion', _set)
                query.select('gender', 'color' + LAYER, 'id', 'location')
                query.where(p.equals('subCat', category))
                t = AnnoyIndex(LAYER_DIMENSION)
                count = 0
                aero_annoy_map = {}
                for (_, _, bins) in query.results():
                    if bins['gender'] == gender and bins['location'] == location:
                        aero_annoy_map[count] = bins['id']
                        t.add_item(count, bins['color' + LAYER])
                        count += 1
                t.build(10)
                write_path = CONFIGS['model_path'] + 'annoy_index_files/' + \
                    _set + '/' + gender + category + LAYER + location
                t.save(write_path + '.ann')
                with open(write_path + '.p', 'wb') as f:
                    pickle.dump(aero_annoy_map, f)


def create_annoy_for_categories(**kwargs):
    ti = kwargs['ti']
    _set = ti.xcom_pull(key='set', task_ids='get_alternate_set')
    _create_annoy_for_categories(_set)


def get_attribute_values(returned='key'):
    with open(os.path.join(CONFIGS['model_path'], CONFIGS['attribute_tree'])) as data_file:
        attribute_tree = json.load(data_file)
    inv_attribute_map = {v: k for k, v in ATTRIBUTE_MAP.items()}
    for child1 in attribute_tree['children']:
        gender = inv_attribute_map[child1[returned]]
        for child2 in child1['children']:
            gender_val = inv_attribute_map[child2[returned]]
            for child3 in child2['children']:
                category = inv_attribute_map[child3[returned]]
                for child4 in child3['children']:
                    category_val = inv_attribute_map[child4[returned]]
                    for child5 in child4['children']:
                        attribute = inv_attribute_map[child5[returned]]
                        for child6 in child5['children']:
                            attribute_val = inv_attribute_map[child6[returned]]
                            for location in COUNTRIES:
                                yield gender_val, category_val, attribute, attribute_val, ATTRIBUTE_LENGTH[attribute], location


def _create_annoy_for_filters(_set):
    import aerospike.predicates as p
    for gender_val, category_val, attribute, attribute_val, attribute_len, location in get_attribute_values():
        query = client.query('fashion', _set)
        query.select('gender', attribute + LAYER, attribute, 'id', 'location')
        query.where(p.equals('subCat', category_val))

        t = AnnoyIndex(attribute_len)
        count = 0
        aero_annoy_map = {}
        start = time.time()

        for (key, meta, bins) in query.results():
            if bins['gender'] == gender_val and bins[attribute] == attribute_val and bins['location'] == location:
                aero_annoy_map[count] = bins['id']
                t.add_item(count, bins[attribute + layer])
                count += 1
        t.build(10)
        write_path = CONFIGS['model_path'] + 'annoy_index_files/' + _set + '/' + \
            gender_val + category_val + attribute_val + location + LAYER
        t.save(write_path + '.ann')
        with open(write_path + '.p', 'wb') as f:
            pickle.dump(aero_annoy_map, f)


def create_annoy_for_filters(**kwargs):
    ti = kwargs['ti']
    _set = ti.xcom_pull(key='set', task_ids='get_alternate_set')
    _create_annoy_for_filters(_set)


def _get_current_set():
    st = '/set'
    s = Server(CONFIGS['query_host'], str(CONFIGS['query_port']))
    current_set_name = s.return_response(st)['set']
    assert current_set_name in ['one', 'two']
    return current_set_name


def _get_alternate_set():
    current_set_name = _get_current_set()
    return {'one': 'two', 'two': 'one'}[current_set_name]


def get_alternate_set(**kwargs):
    alternate_set_name = _get_alternate_set()
    kwargs['ti'].xcom_push(key='set', value=alternate_set_name)


t1 = PythonOperator(
    task_id='get_alternate_set',
    provide_context=True,
    python_callable=get_alternate_set,
    dag=UPDATE_DB_DAG)

t2 = PythonOperator(
    task_id='empty_aero_set',
    provide_context=True,
    python_callable=empty_aero_set,
    dag=UPDATE_DB_DAG)

t3 = PythonOperator(
    task_id='mongo2aero',
    provide_context=True,
    python_callable=mongo2aero,
    dag=UPDATE_DB_DAG)

t4 = PythonOperator(
    task_id='create_annoy_for_categories',
    provide_context=True,
    python_callable=create_annoy_for_categories,
    dag=UPDATE_DB_DAG)

t5 = PythonOperator(
    task_id='create_annoy_for_filters',
    provide_context=True,
    python_callable=create_annoy_for_filters,
    dag=UPDATE_DB_DAG)

t6 = PythonOperator(
    task_id='restart_server',
    provide_context=True,
    python_callable=restart_server,
    dag=UPDATE_DB_DAG)

t1 >> t2 >> t3 >> t4 >> t5 >> t6
