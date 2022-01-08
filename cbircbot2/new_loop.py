from cbircbot2.core.client_twisted import BotFactory
from cbircbot2.core.config import Config


import traceback
from twisted.internet import reactor

def main():
    config = Config()
    config.load()
    try:
        conn = BotFactory(config)
        reactor.connectTCP(conn.hostname, conn.port, conn)
        reactor.run()
    except Exception as e:
        print(f"Exception: {e}")
        traceback.print_exc()
        reactor.stop()
        raise SystemExit()
