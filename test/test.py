import sys
import os
import inspect

# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)
   
# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../flowit")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)

from Brick import Brick
from Buffer import Buffer

brick1 = Brick(0, 1)
brick2 = Brick(1, 0)
brick3 = Brick(1, 0)
buf1 = Buffer()
brick1.SetOut(0, buf1)
brick2.SetIn(0, buf1)
brick3.SetIn(0, buf1)

brick1.DoCycle()