
import multiprocessing as mp
import threading
import re
class InputText(object):
    def __init__(self, parent = None):
        self.parent = parent
        self.queue = mp.Queue()



        self.process = mp.Process(target=self.queue_processing, args=(self.queue, self.parent,))
        #self.process.daemon = True
        self.process.start()


    def queue_processing(self, proc_queue, irc):

        while True:
            msg = proc_queue.get()

            if not re.match('^(.+[aA-zZ0-0])$', msg):
                continue

            irc.msg_to(self.parent.params.CHANNEL, msg + '\r\n')
            out = " {chan}: Bot Says: {msg}".format(chan=self.parent.params.CHANNEL,msg=msg)
            print(out)
