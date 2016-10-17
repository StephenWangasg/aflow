from config import model_path, collection
import cPickle as pickle
from utils import Server
import subprocess, time
from annoy import AnnoyIndex
from data import namespace, client, categories, layer_dimension, layer, attribute_tree, inv_attribute_map, attribute_lengths, locations

def create_aero_master(_set):
    for idx in range(100000000):
        key = (namespace, _set, str(idx))
        try:
            client.remove(key)
        except:
            break

    m = {}
    for idx, product in enumerate(collection.find({'extracted':True})):
        records = idx
        if int(records) % 25000 == 0:
            print str(records) + " ingested"
        key = (namespace, _set, str(idx))
        bins = {}
        for k in product:
            if ('FC7' in k) or ('FC6' in k) or (k=='discounted_price') or (k=='product_url_hash'):
                pass
            else:
                bins[k] = product[k]
 
        bins['id'] = idx
        bins.pop('_id')
        client.put(key, bins)
       
        m[bins['hashedId']] = bins['id']
    with open(model_path + 'annoy_index_files/'+ _set + '/'+ 'hashedIdmap.p', 'wb') as f:
        pickle.dump(m, f)


def build_annoy_index(_set):
    import aerospike.predicates as p
    for gender in ['m', 'f']:
        for category in categories.keys():
            for location in locations:
                query = client.query(namespace, _set)
                query.select('gender', 'color'+layer, 'id', 'location')
                query.where( p.equals('subCat', category) )
                t = AnnoyIndex(layer_dimension)
                count = 0
                aero_annoy_map = {}
                for (key, meta, bins) in query.results():
                    if bins['gender'] == gender and bins['location'] == location:
                        aero_annoy_map[count] = bins['id']
                        t.add_item(count, bins['color' + layer])
                        count += 1
                t.build(10)
                write_path = model_path + 'annoy_index_files/' + _set + '/' + gender + category + layer + location
                t.save(write_path + '.ann')
                with open(write_path + '.p', 'wb') as f:
                    pickle.dump(aero_annoy_map, f)


def get_attribute_values(returned = 'key'):
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
                            for location in locations:
                                yield gender_val, category_val, attribute, attribute_val, attribute_lengths[attribute], location



def build_annoy_index_all_filter(_set):
    import aerospike.predicates as p
    for gender_val, category_val, attribute, attribute_val, attribute_len, location in get_attribute_values():
        query = client.query(namespace, _set)
        query.select('gender', attribute + layer, attribute, 'id', 'location')
        query.where(p.equals('subCat', category_val))

        t = AnnoyIndex(attribute_len)
        count = 0
        aero_annoy_map = {}
        print "Querying ", gender_val, category_val, attribute_val, location
        start = time.time()

        for (key, meta, bins) in query.results():
            if bins['gender'] == gender_val and bins[attribute] == attribute_val and bins['location'] == location:
                aero_annoy_map[count] = bins['id']
                t.add_item(count, bins[attribute + layer])
                count += 1
        t.build(10)
        write_path = model_path + 'annoy_index_files/' + _set + '/' + gender_val + category_val + attribute_val + location + layer
        t.save(write_path + '.ann')
        with open(write_path + '.p', 'wb') as f:
            pickle.dump(aero_annoy_map, f)
        print "Time : ", time.time() - start, " Count : ", count


def load_db_create_index(_set_):
    create_aero_master(_set_)
    build_annoy_index(_set_)
    build_annoy_index_all_filter(_set_)

def get_set_load_index():
    st = '/set'
    s = Server(query_server['host'], query_server['port'])
    set_name = jsons.return_response(st)
    if set_name == 'one':
        load_db_create_index('two')
    elif set_name == 'two':
        load_db_create_index('two')
    else:
        print "something wrong"


if __name__ == "__main__":
    pass

