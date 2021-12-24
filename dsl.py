#!/usr/bin/python3

import argparse
import datetime
import heapq
import logging
import os
import sys

def file_list_by_mtime(rootfolder):
    
    file_list = []    
    
    for dirname, dirnames, filenames in os.walk(rootfolder):
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            if os.path.islink(file_path):
                logging.debug('[{}] added to file_list'.format(file_path))
                os.unlink(file_path)
            else:
                file_list.append(file_path)
                logging.debug('[{}] unlinked'.format(file_path))

    return sorted(file_list, key = lambda fn: os.stat(fn).st_mtime)
    #return heapq.nsmallest(count, file_list, key=lambda fn: os.stat(fn).st_mtime)

def remove_empty_directories(path, remove_root=True):
    
    if not os.path.isdir(path):
        return

    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
          #  print(fullpath)
            if os.path.isdir(fullpath):
                remove_empty_directories(fullpath)
                
    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and remove_root:
        if os.path.islink(path):
            os.unlink(path)
            logging.debug('Unlinking syslink to folder'.format(path))
        else:
            logging.info('Removing empty folder: {}'.format(path))
            os.rmdir(path)

def remove_file_by_size_limit(file_list: list, size_limit: int, path: str):
    
    total_size = 0
    
    for single_file in file_list:
        total_size += os.stat(single_file).st_size
    logging.info('total_size of path: {} MB'.format(round(total_size / 1024 / 1024, 1)))
  #  for single_file in file_list:
  #      print(datetime.datetime.fromtimestamp(os.stat(single_file).st_mtime).strftime('%Y-%m-%d %H:%M:%S'), '{} MB'.format(round(os.stat(single_file).st_size / 1024 / 1024, 1)), single_file)
    
    for single_file in file_list:
        logging.debug('[{}] total size: {} vs size limit: {},'.format(path[-20 if len(path) > 20 else len(path) * -1:], total_size, size_limit), end=' ')
        if size_limit <= total_size: 
            try:   
                single_file_size = os.stat(single_file).st_size
                single_file_mtime =  datetime.datetime.fromtimestamp(os.stat(single_file).st_mtime).strftime('%Y-%m-%d %H:%M')
                
                os.remove(single_file)
                logging.info('[{}] File [{}] is removed. Size: {} MB, modification time: {}'.format(path[-20 if len(path) > 20 else len(path) * -1:], 
                single_file, round(single_file_size / 1024 / 1024, 1), single_file_mtime))

                total_size -= single_file_size                
            except:
                logging.error('[{}] Failed to remove {}. Reason: {}'.format(path[-20 if len(path) > 20 else len(path) * -1:], single_file, sys.exc_info()))
        else:
            logging.info('[{}] size limit is met, current total_size: {} MB'.format(path[-20 if len(path) > 20 else len(path) * -1:], round(total_size / 1024 / 1024, 1)))
            break


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument('--path', dest='path', required=True, help="The path of directory where size limit policy will be enforced")
    ap.add_argument('--size-limit', dest='size-limit', required=True, help="The maximum size allowed of the given path (expressed in MB)")
    ap.add_argument('--debug', dest='debug', action='store_true', help="Enable verbose debug output")
    args = vars(ap.parse_args())
    
    path = str(args['path'])
    debug_mode = args['debug']
    
    try:
        size_limit = int(args['size-limit']) * 1024 * 1024
        if size_limit < 0:
            raise ValueError()
    except:
        print('size-limit cannot be {}'.format(args['size-limit']))
        return        
        
    if os.path.isdir(path) == False:
        print('path {} is not a directory'.format(path))
        return    

    logfile_path = os.path.join(os.environ['HOME'], 'log/dir-size-limiter.log')
    logging.basicConfig(
        filename=logfile_path,
        level=logging.DEBUG if debug_mode else logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.info('dir-size-limiter started')
    
    if debug_mode == True:
        print('Running in debug mode')
        logging.info('Running in debug mode')
    else:
        logging.info('Running in production mode')   
    
    logging.info('path: {}, size-limit: {} MB'.format(path, round(size_limit / 1024 / 1024, 1)))
    
    logging.info('Loading directory content by modification time...')
    file_list = file_list_by_mtime(path)
    for single_file in file_list:
        logging.debug('[...{}] {}'.format(path[-20 if len(path) > 20 else len(path) * -1:], file_list))
    remove_file_by_size_limit(file_list, size_limit, path)
    remove_empty_directories(path, False)
    logging.info('dir-size-limiter finished')
    
if __name__ == '__main__':
        
    main()
