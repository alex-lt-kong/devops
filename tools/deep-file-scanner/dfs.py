#!/usr/bin/python3

import argparse
import os
import random

excluded_words = ['/JunHe']

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument('--path', dest='path', required=True, help="The path of directory in which files would be renamed")
    args = vars(ap.parse_args())
    path = str(args['path'])
    
    if os.path.isdir(path) == False:
        print('[{}] is NOT a valid directory path'.format(path))
        quit()

    files = []
    matched_count = 0
    path_depth = path.count('/')

    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))

    for file in files:
        file_depth = file.count('/')
        if file_depth - path_depth >= 10:   # According to my analysis, 11 is the threshold which rsync.net is compatible to
            excluded = False
            for excluded_word in excluded_words:
                if excluded_word in file:
                    excluded = True
                    break
            if excluded == False:
                print('[{:2}] {}'.format(file_depth - path_depth, file))
                matched_count += 1

    if matched_count == 0:
        if random.randint(0, 10) == 0:
            print('No files which are considered too deep to rsync.net\'s file system.')
    else:
        print('A total of {} file(s)\'s path are considered too deep.'.format(matched_count))

if __name__ == '__main__':
        
    main()
