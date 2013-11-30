import os


INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

def make_dir(dir_path):
    #Ref: http://code.activestate.com/recipes/82465-a-friendly-mkdir/
    try:
        if os.path.exists(dir_path):
            pass
        else:
            head, tail = os.path.split(dir_path)
            if head and not os.path.isdir(head):
                make_dir(head)
            if tail:
                os.mkdir(dir_path)    
    except Exception, e:
        raise e   

class BaseConfig(object):

    CSRF_ENABLED = True
    DEBUG = False

    SECRET_KEY = 'c3ntip3d3'

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
    make_dir(LOG_FOLDER)

    SERVER_LOGFILE = os.path.join(LOG_FOLDER, 'server.log')

    LOCATION_DB_SERVER = "localhost"
    LOCATION_DB = "centipede"
    LOCATION_DB_COLLECTION = "locations"
    