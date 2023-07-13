import getopt
import selectors
import socket
import sys
import asyncio
import time
from contextlib import  suppress
from multiprocessing import Process, JoinableQueue, Manager, Pool
import cbircbot2.core.config
from cbircbot2.core.client import IrcClient
from cbircbot2.core.params import EnvironmentParams
from cbircbot2.core.sockets import Socket
import errno


class CbIrcBot:
    def __init__(self):

        self.ssl_enable: bool = False
        self.cfg: cbircbot2.core.config.Config = cbircbot2.core.config.Config()
        self._is_closed: bool = False
        self.environment_params: EnvironmentParams = EnvironmentParams()
        self.environment_params.load_from_config(self.cfg)
        self.sock = Socket(self.environment_params.HOSTNAME, self.environment_params.PORT, self.ssl_enable)  # force false while im fixing
        self.selector = None
        self.irc = IrcClient(self.sock, self.environment_params)
        self.data_queue: JoinableQueue = JoinableQueue()

        self.process = Process(target=self.irc.process_modules_worker, args=(self.data_queue,))
        #self.process.daemon = True

        self.selector = selectors.DefaultSelector()
        
        if not self.cfg.check_config_exists():
            raise FileNotFoundError("Config Not Found, please copy config.conf.skel to config.cfg")

        try:
            opts, args = getopt.getopt(sys.argv[1:], "s:v",["ssl"])
        except getopt.GetoptError as ge:
            print(f"invalid options provided -  {ge}")
            sys.exit(-1)

        for opt, a, in opts:
            if opt in ('-s', '--ssl'):
                self. ssl_enable = True
                self.cfg.set('SERVER', 'enable_ssl', self.ssl_enable)

        self.environment_params.load_from_config(self.cfg)
        self.ssl_enable = self.environment_params.SSL_ENABLED
        
    def start(self):
      
        if not self.sock.connect():
            raise socket.error(f"Socket cannot connect to {self.environment_params.HOSTNAME}:{self.environment_params.PORT}")
        self.selector.register(self.sock.socket_handler, selectors.EVENT_READ, self.sock.recv)
    
    def unload(self):
        self.selector.close()
        self.process.join()
        self.process.close()
        self.sock.close()
    def get_data(self):
        
        try:
            data = self.sock.recv()
            return data
        except socket.error as e:
            error = e.args[0]
            
            if error == errno.EAGAIN or error == errno.EWOULDBLOCK:
                time.sleep(1)
                return ""
        return ""
        
    def loop(self):
        self.process.start()
        self.irc.auth()
        
        while not self._is_closed:
            
            try:
                data = self.get_data()
                data = data.decode("utf-8")
                
                if not data:
                    continue
                    
                self.irc.bot_loop(data)
                self.data_queue.put((self.irc, data))
                time.sleep(0.1)
            except AttributeError as ae:
                time.sleep(1)
                continue
           
            except KeyboardInterrupt as e:
                IrcClient.write_out("Keyboard Interrupted.. Closing")
                time.sleep(3)
                self.sock.close()
                break
            
            else:
                if not self.process.is_alive():
                    self.irc.write_error("Main Process is Dead. Starting  Now..")
                    self.process.join()
                    self.process.kill()
                    self.process.close()
                    
                    del self.process
                    
                    self.process = Process(target=self.irc.process_modules_worker, args=(self.data_queue,))
                    self.process.start()
                    #self.process.daemon = True
                    
                    if self.process.is_alive():
                        self.irc.write_error("Process Ressurrected!")
                        continue
    
    """
    def loop(self):
        self.process.start()
        self.irc.auth()
        while not self._is_closed:
            event = self.selector.select()
            data = None
            if event:
                for key, mask in event:
                    callback = key.data
                    data = callback(key.fileobj)
                    
                    if data:
                        data = data.decode('utf-8')
                        
                        self.data_queue.put((self.irc, data))
                        self.irc.bot_loop(data)
                        
                        if not self.process.is_alive():
                            try:
                                print("Message loop Process Restarted after Exception")
                                self.process.kill()
                                self.process.close()
                                del self.process
                                
                                self.process = Process(target=self.irc.process_modules_worker, args=(self.data_queue,))
                                self.process.start()
                            except Exception as e:
                                    print(f"Exception: {e}")
"""

def main():
    bot = CbIrcBot()
    bot.start()
    bot.loop()
    bot.unload()
    pass


