import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import netCDF4

url = '/data/input/trim-a.nc'
data = netCDF4.Dataset(url)

# variables
x = data.variables['x'][:]
y = data.variables['y'][:]
t = data.variables['time'][-1]

random = data.variables['random'][t-1, :, :]


# plot random data
plt.subplot(1, 1, 1)
fig = plt.figure()
plt.pcolor(x, y, random, cmap='RdBu')
fig.savefig(os.path.join('/', 'data', 'output', 'image.png'), bbox_inches='tight')
plt.close()
