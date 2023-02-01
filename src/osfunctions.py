from os import listdir, mkdir
from os.path import isfile, join


def get_files_list(username):
    path = f'backup/{username}'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files

def create_directory(username):
    parent_dir = "backup/"
    path = join(parent_dir, username)
    mkdir(path)

if __name__ == '__main__':
    create_directory('dragon')

