import json
import time
from threading import Thread, Lock
from queue import Queue
from websocket import WebSocketApp

class WebsocketManager():
    _CONNECT_TIMEOUT_S = 5

    def __init__(self):
        """
        subscribe is a function that's called right after the websocket connects.
        unsubscribe is a function that's called just before the websocket disconnects.

        both subscribe and unsubscribe MUST have one argument, which is an instance of 
        WebsocketManager (see KrakenWsManagerFactory in ws_factories.py for an example).
        """
        self.ws = None
        self.queue = Queue()
        self.url = 'wss://ws-feed.pro.coinbase.com'
        self.start_time = None
        self.connect()

        t = Thread(
            target = self.dump_size,
            daemon = True
        )
        t.start()
    
    def dump_size(self):
        while True:
            if not self.start_time:
                self.start_time = time.time()
            print(f"Messages Received: {self.queue.qsize()}")
            print(f"Messages p/s: {self.queue.qsize()/(time.time() - self.start_time)}")
            time.sleep(1)

    def _on_message(self, ws, message):
        self.queue.put(message)

    def send(self, message):
        """Sends a message over the websocket"""
        self.connect()
        self.ws.send(message)

    def send_json(self, message):
        """Sends a json message over the websocket"""
        self.send(json.dumps(message))

    def _connect(self):
        """Creates a websocket app and connects"""
        assert not self.ws, "ws should be closed before attempting to connect"

        self.ws = WebSocketApp(
            self.url,
            on_message=self._wrap_callback(self._on_message),
        )

        wst = Thread(target=self._run_websocket, args=(self.ws,))
        wst.daemon = True
        wst.start()

        # Wait for socket to connect
        ts = time.time()
        while self.ws and (not self.ws.sock or not self.ws.sock.connected):
            if time.time() - ts > self._CONNECT_TIMEOUT_S:
                self.ws = None
                raise Exception(
                    f"Failed to connect to websocket url {self._get_url()}")
            time.sleep(0.1)

    def _wrap_callback(self, f):
        """Wrap websocket callback"""
        def wrapped_f(ws, *args, **kwargs):
            if ws is self.ws:
                try:
                    f(ws, *args, **kwargs)
                except Exception as e:
                    raise Exception(f'Error running websocket callback: {e}')
        return wrapped_f

    def _run_websocket(self, ws):
        """"Runs the websocket app"""
        try:
            ws.run_forever(ping_interval=30)
        except Exception as e:
            raise Exception(f'Unexpected error while running websocket: {e}')
        finally:
            pass
            # self._reconnect(ws)

    def _reconnect(self, ws):
        """Closes a connection and attempts to reconnect"""
        assert ws is not None, '_reconnect should only be called with an existing ws'
        if ws is self.ws:
            self.ws = None
            ws.close()
            self.connect()

    def connect(self):
        """Connects to the websocket"""
        if self.ws:
            return
        while not self.ws:
            self._connect()
            if self.ws:
                request = \
                    {"type": "subscribe",
                    "channels": [{"name": "full", "product_ids": ["BTC-USD"]}]}
                self.send_json(request)

if __name__ == "__main__":
    ws = WebsocketManager()
    while True:
        1+1