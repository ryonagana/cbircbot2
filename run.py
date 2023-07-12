import cbircbot2
import sys
import pathlib
import os

#from cbircbot2 import default_loop, new_loop
from cbircbot2 import  default_loop
if __name__ == "__main__":
    target_path = pathlib.Path(__file__).parent.parent
    sys.path.append(target_path.__str__())
    default_loop.main()
