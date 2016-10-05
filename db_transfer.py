from config import model_path, collection, aerospike_config
import cPickle as pickle
from tools import Server, scheduler
import subprocess, time, json, aerospike
from annoy import AnnoyIndex

attribute_tree_path = model_path + 'attribute_tree.json'
with open(attribute_tree_path) as data_file:
    attribute_tree = json.load(data_file)

def get_set_name():
    nsfile = open(model_path + 'nsfile.txt', "r")
    set_name = nsfile.read().strip()
    nsfile.close()
    return set_name


set_ = get_set_name()

client = aerospike.client(aerospike_config).connect()
namespace = 'fashion'
sites = ['zalora','yoox', 'lazada']
categories = {
    "tShirts":['color','pattern',"neck","slLen"],
    "shirts":['color','pattern',"neck","slLen"],
    "leggings":['color','pattern',"length"],
    "downJackets":['color','pattern',"neck"],
    "dresses":['color','pattern',"fit","neck","sil","slLen","dressLen"],
    "skirts":['color','pattern',"dressLen","sil"],
    "shorts":['color','pattern',"fit","length"],
    "polo":['color','pattern',"neck","slLen"],
    "jeans":['color','pattern',"fit"],
    "pullovers":['color','pattern',"neck","slLen"],
    "tankTops":['color','pattern',"neck"],
    "cardigans":['color','pattern',"neck","slLen"],
    "hoodies":['color','pattern',"neck","slLen"],
    "trench":['color','pattern',"neck","slLen"],
    "casualPants":['color','pattern',"fit","length"],
    "camis":['color','pattern'],
    "blazers":['color','pattern',"slLen"],
    "rompers":['color','pattern',"fit"],
    "suitPants" :['color']
    }

layer = 'FC8'
layer_dimension = 25

attribute_lengths = {'color':25, 'dressLen':3, 'fit':3, 'gender':2, 'length':3, 'neck':8, 'pattern':8,'sil' :9, 'slLen':3, 'subCat':19}
attribute_map = {"color":"color","black":"black","blue":"blue","white":"white","red":"red","grey":"grey","beige":"beige","darkBlue":"darkBlue","green":"green","lightBlue":"lightBlue","pink":"pink","purple":"purple","yellow":"yellow","darkGreen":"darkGreen","brown":"brown","orange":"orange","darkGrey":"darkGrey","darkRed":"darkRed","rose":"rose","gold":"gold","silver":"silver","lightGrey":"lightGrey","lightGreen":"lightGreen","melonRed":"watermelonRed","camel":"camel","lakeBlue":"lakeBlue","dressLen":"dressLength","knee":"kneeLength","full":"full","mini":"mini","fit":"fit","slim":"slim","loose":"loose","straight":"straight","gender":"gender","m":"male","f":"female","length":"bottomLength","short":"short","neck":"neckLine","o":"oNeck","v":"vNeck","turtle":"turtleNeck","slash":"slashNeck","strapless":"strapless","turnDown":"turnDownCollar","hooded":"hooded","stand":"standCollar","pattern":"pattern","solid":"solid","print":"print","plaid":"plaid","striped":"striped","floral":"floral","polkaDot":"polkaDot","leopard":"leopard","camouflage":"camouflage","sil":"silhouette","aLine":"aLine","sheath":"sheath","pleated":"pleated","ballGown":"ballGown","pencil":"pencil","asymmetrical":"asymmetrical","fitFlare":"fitAndFlare","trumpet":"trumpetAndMermaid","slLen":"sleeveLength","half":"half","sleeveless":"sleeveless","subCat":"category","tShirts":"tShirts","shirts":"shirts","leggings":"leggings","downJackets":"downJackets","dresses":"dresses","skirts":"skirts","shorts":"shorts","polo":"polo","jeans":"jeans","pullovers":"pullovers","tankTops":"tankTops","cardigans":"cardigans","hoodies":"hoodies","trench":"trench","casualPants":"casualPants","camis":"camis","blazers":"blazers","rompers":"jumpSuitsandRompers","suitPants":"suitPants"}
#attribute_map = {"color":"color","black":"black","blue":"blue","white":"white","red":"red","grey":"grey","beige":"beige","darkBlue":"blue","green":"green","lightBlue":"blue","pink":"pink","purple":"purple","yellow":"yellow","darkGreen":"green","brown":"brown","orange":"orange","darkGrey":"grey","darkRed":"red","rose":"rose","gold":"gold","silver":"silver","lightGrey":"grey","lightGreen":"green","melonRed":"red","camel":"beige","lakeBlue":"blue","dressLen":"dressLength","knee":"kneeLength","full":"full","mini":"mini","fit":"fit","slim":"slim","loose":"loose","straight":"straight","gender":"gender","m":"male","f":"female","length":"bottomLength","short":"short","neck":"neckLine","o":"oNeck","v":"vNeck","turtle":"turtleNeck","slash":"slashNeck","strapless":"strapless","turnDown":"turnDownCollar","hooded":"hooded","stand":"standCollar","pattern":"pattern","solid":"solid","print":"print","plaid":"plaid","striped":"striped","floral":"floral","polkaDot":"polkaDot","leopard":"leopard","camouflage":"camouflage","sil":"silhouette","aLine":"aLine","sheath":"sheath","pleated":"pleated","ballGown":"ballGown","pencil":"pencil","asymmetrical":"asymmetrical","fitFlare":"fitAndFlare","trumpet":"trumpetAndMermaid","slLen":"sleeveLength","half":"half","sleeveless":"sleeveless","subCat":"category","tShirts":"tShirts","shirts":"shirts","leggings":"leggings","downJackets":"downJackets","dresses":"dresses","skirts":"skirts","shorts":"shorts","polo":"polo","jeans":"jeans","pullovers":"pullovers","tankTops":"tankTops","cardigans":"cardigans","hoodies":"hoodies","trench":"trench","casualPants":"casualPants","camis":"camis","blazers":"blazers","rompers":"jumpSuitsandRompers","suitPants":"suitPants"}
inv_attribute_map = {v: k for k, v in attribute_map.items()}

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
        query = client.query(namespace, _set)
        query.select('gender','color'+layer, 'id')
        query.where( p.equals('subCat', category) )
        t = AnnoyIndex(layer_dimension)
        count = 0
        aero_annoy_map = {}
        for (key, meta, bins) in query.results():
            if bins['gender'] == gender:
                aero_annoy_map[count] = bins['id']
                t.add_item(count, bins['color' + layer])
                count += 1
        t.build(10)
        write_path = model_path + 'annoy_index_files/' + _set + '/' + gender + category + layer
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
                            yield gender_val, category_val, attribute, attribute_val, attribute_lengths[attribute]


def build_annoy_index_all_filter(_set):
    import aerospike.predicates as p
    for gender_val, category_val, attribute, attribute_val, attribute_len in get_attribute_values():
        query = client.query(namespace, _set)
        query.select('gender', attribute + layer, attribute, 'id')
        query.where(p.equals('subCat', category_val))

        t = AnnoyIndex(attribute_len)
        count = 0
        aero_annoy_map = {}
        print "Querying ", gender_val, category_val, attribute_val
        start = time.time()

        for (key, meta, bins) in query.results():
            if bins['gender'] == gender_val and bins[attribute] == attribute_val:
                aero_annoy_map[count] = bins['id']
                t.add_item(count, bins[attribute + layer])
                count += 1
        t.build(10)
        write_path = model_path + 'annoy_index_files/' + _set + '/' + gender_val + category_val + attribute_val + layer
        t.save(write_path + '.ann')
        with open(write_path + '.p',
                  'wb') as f:
            pickle.dump(aero_annoy_map, f)
        print "Time : ", time.time() - start, " Count : ", count


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
        #publish to restart the server

if __name__ == "__main__":
	create_aero_master('one')
	build_annoy_index('one')
	build_annoy_index_all_filter('one')

