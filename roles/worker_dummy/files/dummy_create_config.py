import os
import sys

from mako.template import Template

step_numbers = sys.argv[1]
target = open(os.path.join('/','data','output','delft3d_config.ini'), 'w')
target.write('[variables]\n')
config = Template("number_steps=${n}")
target.write(config.render(n=step_numbers))
target.close()





