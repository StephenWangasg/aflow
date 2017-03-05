'''minimal configurations for all feeds'''

CONFIGS = {

    'log_path': '/images/models/logs/',
    'mongo_host' : 'localhost',
    'mongo_port' : 27017,
}

DOWNLOAD_CONFIGS = {

    'download_path': '/images/models/feeds/',
    'feed_images_path': '/images/models/feed_images/',
}

def update(op_kwargs):
    'merge minimal configurations into feeds operational conf'
    op_kwargs.update(CONFIGS)
    op_kwargs.update(DOWNLOAD_CONFIGS)

