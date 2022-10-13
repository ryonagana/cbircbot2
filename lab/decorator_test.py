from functools import wraps


class TestWrapper(object):
    def __init__(self,cmd_name):
        self.cmd_name: str = cmd_name
        
    def __call__(self, function, *args, **kwargs):
        def wrapper(*args, **kwargs):
            val = function(*args, *kwargs)
            print(f"{val =}")
            print(f"{args =} {kwargs}")
            return val
        return wrapper
    
@TestWrapper(cmd_name="AUI")
class T2:
    def __init__(self):
        pass
    
    
    
if __name__ == "__main__":
    t = T2()