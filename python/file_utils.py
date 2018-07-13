#-*- coding: utf-8 -*-
#python 3.5
import shutil
import os
import pickle as pkl

def walk_dir_bfs(dir_path):
    list_dirs = os.walk(dir_path)
    for root, dirs, files in list_dirs:
        for d in dirs:
            print(os.path.join(root, d))
        for f in files:
            print(os.path.join(root, f))

def walk_dir_dfs(dir_path):
    for lists in os.listdir(dir_path):
        path = os.path.join(dir_path, lists)
        #print(path)
        if os.path.isdir(path):
            walk_dir_dfs(path)

def dir_traversal(dir_path, only_file=True):
    #获取dir_path目录下的所有文件路径，返回路径list
    file_list = []
    for lists in os.listdir(dir_path):
        path = os.path.join(dir_path, lists)
        if os.path.isdir(path):
            if(only_file == False):
                file_list.append(path)
            file_list.extend(dir_traversal(path))
        else:
            file_list.append(path)
    return file_list


def clear_directory(dir_path, specific_extensions=[]):
    """

    Args:
        dir_path:
        specific_extensions: to delete specific extensions, by default, delete everything (including directory).

    Returns:

    """
    if len(specific_extensions) == 0:
        shutil.rmtree(dir_path, ignore_errors=True)
        os.makedirs(dir_path)
    else:
        file_list = dir_traversal(dir_path)

        for file in file_list:
            for extension in specific_extensions:
                if file.endswith(extension):
                    os.remove(file)
                    break

def load_from_pkl(pkl_path):
    with open(pkl_path, 'rb') as fin:
        obj = pkl.load(fin)
    return obj

def dump_to_pkl(obj, pkl_path):
    with open(pkl_path, 'wb') as fout:
        pkl.dump(obj, fout, protocol=pkl.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    l = dir_traversal("/home/eric-lin/StateGrid/TrajectoriesMining/")
    print(l)
