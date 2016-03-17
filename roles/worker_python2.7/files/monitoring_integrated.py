# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 14:28:54 2016

@author: konin_de

Monitoring file delft3d output
"""

import os
import time
import logging
import sys

from watchdog.observers import Observer

import watcher

logger = logging.getLogger(__name__)

def process_data(filename, shared={"counter": 0}):
    """everything we need to do if a file changes"""

    # We pass a dictionary with shared data, so we can reuse it between calls.
    # global variables are not available because this function is called in a
    # different thread.
    # A more elegant example is to use some shared memory between threads.
    # or create a class with __call__ method

    logger.info('processing %s', filename)
    file_num = "%04d" % (shared["counter"], )
    for task in tasks:
        varname = task['variable']
        fname_nc_proc = '%s_%s.nc' % (varname, file_num)
        fname_png_viz = '%s_%s.png' % (varname, file_num)
        process = task['process']
        viz = task['viz']
        logger.info("calling processing script %s", process)
        try:
            process(fpath_delft3d_data, filename,
                    fpath_proc_data, fname_nc_proc, timestep=-1)
        except:
            logger.exception("Processing failed")
        logger.info("calling visualization script %s", process)
        try:
            viz(fpath_proc_data, fname_nc_proc, fpath_figures, fname_png_viz)
        except:
            logger.exception("Visualization failed")
    shared["counter"] += 1

if __name__ == "__main__":

    variables = sys.argv[1:]

    tasks = []

    sys.path.append(r"/data/")
    sys.path.append(r"/data/trunk/scripts/postprocessing")
    sys.path.append(r"/data/trunk/scripts/visualisation")

    for variable in variables:
        task = {}
        task['variable'] = variable
        task['process_name'] = variable + "_proc"
        task['viz_name'] = variable + "_viz"
        task['process_module'] = __import__(task['process_name'])
        function_name = 'run_' + task['process_name']
        task['process'] = getattr(task['process_module'], function_name)
        task['viz_module'] = __import__(task['viz_name'])
        task['viz'] = getattr(task['viz_module'], 'run_' + task['viz_name'])
        function_name = 'get_var_' + task['process_name']
        task['get_var'] = getattr(task['process_module'], function_name)
        tasks.append(task)
    
    logging.basicConfig(level=logging.INFO)
    observer = Observer()
    handler = watcher.NetCDFHandler()
    
    fpath_delft3d_data = os.path.join('/','data','input')
    fpath_proc_data = os.path.join('/','data','output')
    fpath_figures = os.path.join('/','data','output')
    
    fname_nc = 'trim-a.nc'
    
    handler.processors.append(process_data)
    handler.observer = observer
    handler.fname_nc = fname_nc
    observer.schedule(handler, fpath_delft3d_data, recursive=False)
    observer.start()
    # maximum run time
    try:
        while True:
            if not handler.done:
                time.sleep(1)
            else:
                break
    except KeyboardInterrupt:
        observer.stop()
    except:
        logger.exception("Processing failed, stopping monitoring")
        observer.stop()
    observer.stop()
    observer.join()
