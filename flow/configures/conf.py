'''minimal configurations for all feeds'''

CONFIGS = {

    'log_path': '/images/models/logs/',
}

DOWNLOAD_CONFIGS = {

    'download_path': '/images/models/feeds/',

}

def update(op_kwargs):
    'merge minimal configurations into feeds operational conf'
    op_kwargs.update(CONFIGS)
    op_kwargs.update(DOWNLOAD_CONFIGS)
