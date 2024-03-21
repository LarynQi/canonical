import os
import sys

def rm_dir(path):
    if not os.path.isdir(path):
        return
    for f in os.listdir(path):
        full_path = f'{path}/{f}'
        if os.path.isdir(full_path):
            rm_dir(full_path)
        else:
            os.remove(full_path)
    os.rmdir(path)

def main():
    db_dir = sys.path[0] + '/db/'
    rm_dir(db_dir)
    os.mkdir(db_dir)
    
if __name__ == '__main__':
    main()
