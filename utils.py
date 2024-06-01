from glob import glob
import config
import os

def get_file_by_id(id):
    result = glob(config.PATH_FOR_MEDIA + '????-??-??_' + str(id) + '.*')
    if len(result) == 1:
        return result[0]
    else:
        return None

def delete_file_by_id(id):
    file_name = get_file_by_id(id)
    if file_name is not None:
        os.remove(file_name)
        return True
    else:
        return False
