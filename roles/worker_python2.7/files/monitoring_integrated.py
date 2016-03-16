# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 14:28:54 2016

@author: konin_de

Monitoring file delft3d output
"""

import os
from netCDF4 import Dataset
import time
import subprocess
import sys
from collections import OrderedDict
print sys.path
sys.path.append(r"/data/trunk/scripts/postprocessing") ## TODO: This path should refer to the processing scripts of the checkout
sys.path.append(r"/data/trunk/scripts/visualisation") ## TODO: This path should refer to the visualization scripts of the checkout
print sys.path
variables = sys.argv[1:]

proc_list = list()
viz_list = list()
for variable in variables:
    variable = variable.replace(' ', '_')
    proc_list.append(variable + "_proc")
    viz_list.append(variable + "_viz")
    
#proc_list = ['channel_network_proc'] ## TODO: This list should be provided by the frontend!
#viz_list = ['channel_network_viz'] ## TODO: This list should be provided by the frontend!

proc_dict = OrderedDict()
for item in proc_list:
    exec 'import ' + item
    exec 'proc_dict[' + item + '] = ' + item + '.run_' + item
    
var_dict = OrderedDict()
for item in proc_list:
    exec 'import ' + item
    exec 'var_dict[' + item + '] = ' + item + '.get_var_' + item
    
viz_dict = OrderedDict()    
for item in viz_list:
    exec 'import ' + item
    exec 'viz_dict[' + item + '] = ' + item + '.run_' + item

#import channel_network_proc
#import channel_network_viz

workdir = os.path.join('/','data','input') ## TODO: This path should refer to the output/workdirectory of the Delft3D run
print workdir
logfile = 'delft3d.log' ## TODO: In run_flow2d3d.bat change "%exedir%\d_hydro.exe" %argfile% to --> "%exedir%\d_hydro.exe" %argfile% >delft3d.log 2>&1
                        ## TODO: or in run_flow2d3d.sh (in linux) change to $exedir/d_hydro.exe $argfile >delft3d.log 2>&1

fname_nc_delft3d = 'trim-a.nc' ## TODO: Has to match the name as defined in the frontend/mdf

fpath_delft3d_data = workdir ## TODO: Has to match the location of the delft3d output files (probably = workdir)
fpath_proc_data = os.path.join('/','data','output','processed') ## TODO: Path refers to location where the processed data (.nc) has to be stored
fpath_figures = os.path.join('/','data','output','figures') ## TODO: Path refers to location where the figures are stored.

## timesteps are all in seconds
model_ts = 1200  ## TODO: This has to match with the timestep that is actually used in the model, so perhaps get/read from the frontend/database
output_ts = 43200 ## TODO: This has to match with the output timestep that is actually used in the model, so perhaps get/read from the frontend/database
start_output_ts = 2678400 ## TODO: This has to match with the value that is set in the mdf.
viz_ts = 43200 ## TODO: This has to match with the visualization timestep that is actually defined in the user-interface, so perhaps get/read from the frontend/database

fpath = os.path.join(workdir,logfile)

output_counter = 0
viz_counter = 0
no_timesteps = None

def read_timestamps(fpath_nc):
    with Dataset(fpath_nc, 'r') as nc_fid:
        print nc_fid.variables.keys()
        print nc_fid.variables['time']
        timestamps = nc_fid.variables['time'][:]
    return timestamps

def read_log(fpath, no_timesteps = None):
    with open(fpath, 'r') as ft:
        lines = ft.readlines()
    
    while no_timesteps is None:
        
        with open(fpath, 'r') as ft:
            lines = ft.readlines()
        print "read log file"
        for line in lines:
            if "Time to finish" in line:
                print(line)
                no_timesteps = int(line.strip().split()[-1])
                break
    
    for line in lines[::-1]:
        if "d_hydro shutting down normally" in line:
            sim_finished = True
            current_timestep = no_timesteps
            progress_perc = "100.0%"
            break
        
        elif "Time to finish" in line: 
            print(line)
            sim_finished = False
            current_timestep = no_timesteps - int(line.strip().split()[-1])
            progress_perc = [part for part in line.strip().split() if "%" in part][0]
            break
    
    return (no_timesteps, current_timestep, progress_perc, sim_finished)

print("checking path")
sys.stdout.flush()
no_file = True
while no_file == True:
    if os.path.exists(fpath):
        no_file = False
        print("file exists")
        sys.stdout.flush()
    else:
        no_file = True

while True:
    time.sleep(5)
    print "running script"
    no_timesteps, current_timestep, progress_perc, sim_finished = read_log(fpath, no_timesteps)
    ts_threshold = start_output_ts/model_ts
    ts_before_output = output_ts/model_ts
    ts_before_viz = viz_ts/model_ts

    #ts_check_viz =  ts_threshold + viz_counter * ts_before_viz
    ts_check_viz = 0
    print current_timestep, ts_check_viz, ts_threshold, ts_before_viz
    sys.stdout.flush()
    if current_timestep > ts_check_viz: ## Here > is used instead of >= because of the fact that delft3d is still writing the data while this script is reading it.
        viz_counter += 1
        
        for key, val in var_dict.items():
            variables, varname = val()
            filename, ext = os.path.splitext(fname_nc_delft3d)
            fname_nc_cut_delft3d = ''.join([filename, '_', str(viz_counter), ext])
            sub_args = ["-v time,%s" % ','.join(variables), "-d time,%s" % (viz_counter-1)] ## TODO: Here the correct timestep should be read.
            argument = "ncks %s %s %s %s" % (sub_args[0], sub_args[1],  os.path.join(fpath_delft3d_data, fname_nc_delft3d), os.path.join(fpath_proc_data, fname_nc_cut_delft3d))
            subprocess.call(argument, shell=True)
        
        file_num = "0000"[:-len(str(viz_counter))] + str(viz_counter)
        fname_nc_proc = '%s_%s.nc' % (varname, file_num) ## TODO: maybe the extension should be defined above
        fname_png_viz = '%s_%s.png' % (varname, file_num) ## TODO: maybe the extension should be defined above
        
        timestamps = read_timestamps(os.path.join(fpath_proc_data, fname_nc_cut_delft3d))
        print timestamps, ts_check_viz, model_ts
        timestamp = 2678400
        print timestamp
        ind = list(timestamps).index(timestamp)

        for key, val in proc_dict.items():
            val(fpath_delft3d_data, fname_nc_delft3d, fpath_proc_data, fname_nc_proc, timestep=ind)
        for key, val in viz_dict.items():
            val(fpath_proc_data, fname_nc_proc, fpath_figures, fname_png_viz)
    
    elif current_timestep == no_timesteps and sim_finished == True:
        break
    
#    ts_check_output = ts_threshold + output_counter * ts_before_output
#    if current_timestep >= ts_check_output:
#        output_counter += 1
        ## run scripts


"""
Dit moet worden toegevoegd aan Template processing in plaats van de huidige functie.
Dit is puur zodat het testmodel werkt!!
import numpy as np

    def read_var(self, nc_fid, variable):
        self.missing_variables = list()
        
        if variable in nc_fid.variables.keys():
            dim = nc_fid.variables[variable].shape
            if len(dim) > 3:
                cut_variable = np.zeros(shape =(dim[0],dim[2],dim[3]))
                for i in range(dim[0]):
                    cut_variable[i] = nc_fid.variables[variable][i][0] ## This takes the first layer of the velocity
                
                if self.timestep == 'all':
                    return cut_variable[:]
                elif variable in ['XCOR','YCOR']:
                    return cut_variable[:]
                else:
                    return cut_variable[self.timestep]
                
            if self.timestep == 'all':
                return nc_fid.variables[variable][:]
            elif variable in ['XCOR','YCOR']:
                return nc_fid.variables[variable][:]
            else:
                return nc_fid.variables[variable][self.timestep]
        
        else:
            self.available_var_str = ', '.join(sorted(nc_fid.variables.keys()))
            
            self.missing_variables.append(variable)
            self.variables_missing = True
"""