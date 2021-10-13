import random
import time
from multiprocessing import Process,Queue, current_process, Pool, JoinableQueue
from typing import Any,Dict

class NObject:
    def __init__(self):
        self.lst: list = [j + 10 * 10 for j in range(100) ]

class BigClass(object):
    a = 10
    b = []
    c = NObject()
    
    def __init__(self):
        pass


def str_random(i:int):
    rnd = ""
    for _ in range(i):
        t = random.randint(65,255)
        rnd += (chr(t))
    return rnd


letters = [12,6,11,4,9,5]
proc_list = []


def worker(bigclass: BigClass, queue: JoinableQueue):
    
    while True:
        if queue.empty():
            continue
            
        task = queue.get()
        print(bigclass)
        queue.task_done()


if __name__ == "__main__":
    
    q = JoinableQueue()
    pool = Pool()
    
    big = BigClass()
    
    p = Process(target=worker, args=(big, q,))
    p.start()
    
    while True:
        text = str_random(random.choice(letters))
        q.put((big, text))
        time.sleep(1)
        pass
    