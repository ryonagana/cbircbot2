import cbircbot2
import sys
import pathlib
import os

if __name__ == "__main__":
    target_path = pathlib.Path(__file__).parent.parent
    sys.path.append(target_path)
    cbircbot2.main()
    pass
