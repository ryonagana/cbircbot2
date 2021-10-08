import random
import time
from multiprocessing import Process,Queue, current_process, Pool
from typing import Any,Dict



def str_random(i:int):
    rnd = ""
    for _ in range(i):
        t = random.randint(65,255)
        rnd += (chr(t))
    return rnd


letters = [12,6,11,4,9,5]
proc_list = []


def worker(text:str):
    print(f"QUEUE: {text}")
    time.sleep(1)


if __name__ == "__main__":
    
    q = Queue()
    pool = Pool()
    

    
    while True:
        
        text = str_random(random.choice(letters))
        pool.apply(worker, (text,))
        time.sleep(1)
        pass
    