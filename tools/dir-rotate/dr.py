#!/usr/bin/python3

import argparse
import datetime as dt
import logging
import os
import sys


def file_list_by_mtime(rootfolder):
    
    file_list = []    
    
    for dirname, dirnames, filenames in os.walk(rootfolder):
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            if os.path.islink(file_path):
                logging.debug('[{}] unlinked'.format(file_path))
                os.unlink(file_path)
            else:
                file_list.append(file_path)
                logging.debug('[{}] added to file_list'.format(file_path))

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
        try:
            total_size += os.stat(single_file).st_size
        except Exception as ex:
            logging.error(f'error os.stat()ing: {ex}')
    logging.info(f'total_size of path: {round(total_size / 1024 / 1024, 1)} MB')

    
    for single_file in file_list:
        logging.debug(
            f'[{path[-20 if len(path) > 20 else len(path) * -1:]}] '
            f'total size: {total_size} vs size limit: {size_limit}, ',
            end=' '
        )
        if size_limit <= total_size: 
            try:   
                single_file_size = os.stat(single_file).st_size
                single_file_mtime =  dt.datetime.fromtimestamp(
                    os.stat(single_file).st_mtime
                ).strftime('%Y-%m-%d %H:%M')
                
                os.remove(single_file)
                logging.info(
                    f'[{path[-20 if len(path) > 20 else len(path) * -1:]}] '
                    f'File [{single_file}] is removed. '
                    f'Size: {round(single_file_size / 1024 / 1024, 1)} MB, '
                    f'modification time: {single_file_mtime}'
                )

                total_size -= single_file_size                
            except:
                logging.error(
                    f'[{path[-20 if len(path) > 20 else len(path) * -1:]}] '
                    f'Failed to remove {single_file}. Reason: {sys.exc_info()}'
                )
        else:
            logging.info(
                f'[{path[-20 if len(path) > 20 else len(path) * -1:]}] size limit is met, '
                f'current total_size: {round(total_size / 1024 / 1024, 1)} MB'
            )
            break


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument(
        '--path', dest='path', required=True,
        help="The path of directory where size limit policy will be enforced"
    )
    ap.add_argument(
        '--size-limit', dest='size-limit', required=True,
        help="The maximum size allowed of the given path (expressed in MB)"
    )
    ap.add_argument(
        '--debug', dest='debug', action='store_true',
        help="Enable verbose debug output"
    )
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
        
    if os.path.isdir(path) is False:
        raise RuntimeError(f'Path [{path}] is not a directory')
        return    

    logfile_path = os.path.join(os.environ['HOME'], 'log/dir-rotate.log')
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if debug_mode else logging.INFO,
        format='%(asctime)s|%(levelname)7s|%(funcName)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.info('dir-rotate started')
    
    if debug_mode:
        print('Running in debug mode')
        logging.info('Running in debug mode')
    else:
        logging.info('Running in production mode')   
    
    logging.info(
        f'path: {path}, size-limit: {round(size_limit / 1024 / 1024, 1)} MB'
    )
    
    logging.info('Loading directory content by modification time...')
    file_list = file_list_by_mtime(path)
    for _ in file_list:
        logging.debug(f'[...{path[-20 if len(path) > 20 else len(path) * -1:]}] {file_list}')
    remove_file_by_size_limit(file_list, size_limit, path)
    remove_empty_directories(path, False)
    logging.info('dir-rotate finished')
    
if __name__ == '__main__':
        
    main()
