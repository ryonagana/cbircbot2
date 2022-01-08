import cbircbot2
import sys
import pathlib
import os

from cbircbot2 import default_loop, new_loop

if __name__ == "__main__":
    target_path = pathlib.Path(__file__).parent.parent
    sys.path.append(target_path)
    

    new_loop_active = os.getenv('CB_NEW_LOOP')

    if not new_loop_active or new_loop_active == '0' :
        default_loop.main()
    else:
        new_loop.main()
    pass
