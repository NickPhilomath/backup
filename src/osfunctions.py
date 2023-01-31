from os import listdir
from os.path import isfile, join


def get_files_list(username):
    path = f'backup/{username}'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files



if __name__ == '__main__':
    get_files_list('nick')

