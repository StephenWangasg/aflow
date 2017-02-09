import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.target_downloader import target_download
from flow.parsers.target_parser import parse_write
from flow.config import data_feed_path
from flow.dags.utils import target_args, get_sub_dag


dag = DAG('target', default_args=target_args)

website = 'target'
country = 'global'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'new_parsed_csv': p + 'current.csv',
    'website': website,
    'country': country,
    'map': [
        ('product_name', 'Product Name'),
        ('product_url', 'Product URL'),
        ('image_url', 'Image URL'),
        ('unique_url', 'Image URL')
    ],
    'cats': [
        "Apparel & Accessories > Clothing > Dresses",
        "Apparel & Accessories > Clothing > One-Pieces",
        "Apparel & Accessories > Clothing > One-Pieces > Leotards & Unitards",
        "Apparel & Accessories > Clothing > One-Pieces > Jumpsuits & Rompers",
        "Apparel & Accessories > Clothing > One-Pieces > Overalls",
        "Apparel & Accessories > Clothing > Outerwear",
        "Apparel & Accessories > Clothing > Outerwear > Coats & Jackets",
        "Apparel & Accessories > Clothing > Outerwear > Snow Pants & Suits",
        "Apparel & Accessories > Clothing > Outerwear > Vests",
        "Apparel & Accessories > Clothing > Outfit Sets",
        "Apparel & Accessories > Clothing > Pants",
        "Apparel & Accessories > Clothing > Shirts & Tops",
        "Apparel & Accessories > Clothing > Shorts",
        "Apparel & Accessories > Clothing > Skirts",
        "Apparel & Accessories > Clothing > Skorts",
        "Apparel | Activewear | Activewear Bottoms | Activewear Leggings",
        "Apparel | Activewear | Activewear Shirts | Activewear Sweatshirt",
        "Apparel | Bottoms | Combination Bottoms | Scooters",
        "Apparel | Bottoms | Combination Bottoms | Skorts",
        "Apparel | Bottoms | Coveralls and Jumpsuits | Coveralls",
        "Apparel | Bottoms | Pants | Cargo Pants",
        "Apparel | Bottoms | Pants | Chino Pants",
        "Apparel | Bottoms | Pants | Fashion Pants",
        "Apparel | Bottoms | Pants | Jeans",
        "Apparel | Bottoms | Pants | Jogger Pants",
        "Apparel | Bottoms | Pants | Legging Pants",
        "Apparel | Bottoms | Pants | Lounge Pants",
        "Apparel | Bottoms | Pants | Pull-on Pants",
        "Apparel | Bottoms | Pants | Trousers",
        "Apparel | Bottoms | Shorts | Chino Shorts",
        "Apparel | Bottoms | Skirts | A Line Skirts",
        "Apparel | Bottoms | Skirts | Maxi Skirts",
        "Apparel | Collection And Coordinate Sets | Coordinate Sets | Top and Bottom Sets",
        "Apparel | Dresses | Dresses | A Line Dresses",
        "Apparel | Dresses | Dresses | Jumpers",
        "Apparel | Dresses | Dresses | Shirt Dresses",
        "Apparel | Tops | Jackets | Fashion Jackets",
        "Apparel | Tops | Jackets | Suit Coats",
        "Apparel | Tops | Shirts | Blouses",
        "Apparel | Tops | Shirts | Button Down Shirts",
        "Apparel | Tops | Shirts | Henley Shirts",
        "Apparel | Tops | Shirts | Peasant Tops",
        "Apparel | Tops | Shirts | Polo Shirts",
        "Apparel | Tops | Shirts | Sweatshirts",
        "Apparel | Tops | Shirts | Tank Tops",
        "Apparel | Tops | Shirts | Tee Shirts",
        "Apparel | Tops | Shirts | Tunics",
        "Apparel | Tops | Sweaters | Cardigans",
        "Apparel | Tops | Sweaters | Pullover Sweaters"
    ]
}

t1 = PythonOperator(
    task_id='download_target',
    provide_context=True,
    python_callable=target_download,
    op_kwargs=op_kwargs,
    dag=dag)


t2 = PythonOperator(
    task_id='parse_target',
    provide_context=True,
    python_callable=parse_write,
    op_kwargs=op_kwargs,
    dag=dag)

t3 = get_sub_dag(op_kwargs, dag)

t1 >> t2 >> t3