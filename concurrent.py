class Channel:
    """An implementation of a clojure-like channel.
    https://clojure.org/guides/async_walkthrough
    https://clojure.org/news/2013/06/28/clojure-clore-async-channels

    Built on top of python queue.Queue, which uses a mutex with 
    a deque under the hood.
    
    Args:
        maxsize: the maximum number of items in the channel.
            - 0 is inf buffer, 1 is unbuffered (rendezvous), >1 is a n-buffer.
        mode: the mode of the channel
            - default: blocking put, blocking get
            - dropping: drop newest values when buffer is full
            - sliding: drop oldest values when buffer is full

    Methods:
        put(item: Any) -> None:
            Put an item into the channel (blocking).
        get() -> Any:
            Get an item from the channel (blocking).
        drain() -> list[Any]:
            Drain the channel, returning a list of items.
    """
    # TODO: add a close sentinel?

    def __init__(self, maxsize: int = 10, mode: str = "default"):
        if mode not in ["default", "dropping", "sliding"]:
            raise ValueError(f"Invalid mode: {mode}")
        self._maxsize = maxsize
        self._mode    = mode
        self._chan    = queue.Queue(maxsize=maxsize)
        self._lock    = threading.Lock()
    
    def put(self, item: Any) -> None:
        # default: blocking put, blocking get
        if self._mode == "default":
            self._chan.put(item, block=True)
            return None
        # dropping: drop newest values when buffer is full
        if self._mode == "dropping":
            try: 
                self._chan.put(item, block=False)
            except queue.Full: 
                pass
            return None
        # sliding: drop oldest values when buffer is full
        if self._mode == "sliding":
            with self._lock:
                try:
                    self._chan.put(item, block=False)
                except queue.Full:
                    try:
                        self._chan.get(block=False)
                    except queue.Empty:
                        pass
                    self._chan.put(item, block=False)
            return None

    def get(self) -> Any:
        return self._chan.get(block=True)
    
    def drain(self) -> list[Any]:
        items = []
        while True:
            try:
                items.append(self._chan.get(block=False))
            except queue.Empty:
                break
        return items
