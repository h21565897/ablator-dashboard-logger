import threading
from typing import List, Dict, Tuple, Set, Optional, Any, Callable, Union
import httpx
import sys
import time
from logger_message import Message

# Create a lock object
lock = threading.Lock()


class LoggerBuffer:
    bufferStore: List[Dict[str, any]]
    len: int

    def __init__(self):
        self.bufferStore = []
        self.len = 0
        threading.Thread(target=self.check_thread).start()

    def append(self, data: Message):
        lock.acquire()
        self.bufferStore.append(data.to_json())
        self.len += 1
        if sys.getsizeof(self.bufferStore) > 50000:
            self.flush()
        lock.release()

    def check_thread(self):
        while True:
            time.sleep(5)
            lock.acquire()
            self.flush()
            lock.release()

    async def flush(self):
        async with httpx.AsyncClient() as client:
            for data in self.bufferStore[:]:
                await client.post("http://localhost:8000", json=data)
                self.bufferStore.remove(data)
