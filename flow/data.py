from config import model_path, aerospike_config
import json, aerospike

attribute_tree_path = model_path + 'attribute_tree.json'
with open(attribute_tree_path) as data_file:
    attribute_tree = json.load(data_file)

def get_set_name():
    nsfile = open(model_path + 'nsfile.txt', "r")
    set_name = nsfile.read().strip()
    nsfile.close()
    return set_name


set_ = get_set_name()
locations = ['singapore', 'indonesia', 'malaysia', 'global']
sites = ['zalora','yoox', 'lazada', 'asos', 'farfetch']

client = aerospike.client(aerospike_config).connect()
namespace = 'fashion'
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