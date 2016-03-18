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
import json
import subprocess
import shlex
import functools

from collections import OrderedDict
from watchdog.observers import Observer
import netCDF4

import watcher

logger = logging.getLogger(__name__)

def process_data(filename, shared={"counter": 0, "current": 0}):
    """everything we need to do if a file changes"""

    # We pass a dictionary with shared data, so we can reuse it between calls.
    # global variables are not available because this function is called in a
    # different thread.
    # A more elegant example is to use some shared memory between threads.
    # or create a class with __call__ method
    fpath_delft3d_nc = os.path.join(fpath_delft3d_data, filename)
    with netCDF4.Dataset(fpath_delft3d_nc) as ds:
        if ds.variables['time'].shape[0] > 0:
            timesteps = ds.variables['time'][:]
        else:
            logger.info("No timesteps available in netCDF.")
            return

    if timesteps.shape[0] < 2:
        logger.info("Waiting for two output time steps.")
        return

    if timesteps.shape[0] - 1 > shared["current"]:
        shared["current"] = timesteps.shape[0] - 1
    else:
        logger.info("Figure is already being created.")
        return

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
                    fpath_proc_data, fname_nc_proc, timestep=shared["current"])
        except:
            logger.exception("Processing failed")
        logger.info("calling visualization script %s", process)
        try:
            viz(fpath_proc_data, fname_nc_proc, fpath_figures, fname_png_viz)
        except:
            logger.exception("Visualization failed")
        try:
            write_json(fpath_figures, variables, file_num)
        except:
            logger.exception("Creating json-log failed")
    shared["counter"] += 1

def write_json(fpath_fig, varnames, file_num):
    logger.info("Creating log-file json")
    dirlist = os.listdir(fpath_fig)
    log_json = {}
    log_json['logfile'] = 'input/delft3d.log'
    log_json['progress'] = int(file_num)

    for varname in varnames:
        figure_list = []
        for fname in dirlist:
            filename, ext = os.path.splitext(fname)
            if filename.startswith(varname) and ext == ".png":
                figure_list.append(fname)

        name = varname + '_images'
        log_json[name] = OrderedDict()
        log_json[name]['location'] = ''
        log_json[name]['images'] = sorted(figure_list)

    with open(os.path.join(fpath_figures, 'log_json.json'), 'w') as jsfile:
        json.dump(log_json, jsfile)


def on_done(filename):
    """zip file when done"""
    logger.info("zipping and removing filename: %s", filename)
    old_name = filename
    name, ext = os.path.splitext(old_name)
    new_name = name + '_z' + ext
    # split command for the call
    cmd = "nc3tonc4 -o --classic=1 --zlib=1 '%s' '%s'" % (old_name, new_name)
    shlex.split(cmd)
    # call in a subshell so we have the environment
    subprocess.call(cmd, shell=True)
    os.remove(old_name)

if __name__ == "__main__":

    variables = sys.argv[1:]
    logging.basicConfig(level=logging.INFO)
    tasks = []

    sys.path.append(r"/data/")
    sys.path.append(r"/data/tag0.1/scripts/postprocessing")
    sys.path.append(r"/data/tag0.1/scripts/visualisation")

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

    logger.info(tasks)
    observer = Observer()
    handler = watcher.NetCDFHandler()
    
    fpath_delft3d_data = os.path.join('/', 'data', 'input')
    fpath_proc_data = os.path.join('/', 'data', 'output')
    fpath_figures = os.path.join('/', 'data', 'output')
    fname_nc = 'trim-a.nc'
    
    handler.processors.append(process_data)
    on_done = functools.partial(on_done, fname_nc)
    handler.done_handlers.append(on_done)
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
