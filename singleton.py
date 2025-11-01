import logging
import threading

logging.basicConfig(
    level=logging.DEBUG,  # Capture all logs from DEBUG and above
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()


class Obj:
    """Example singleton class using __new__ only.

    Stores provided positional arguments and keyword arguments and exposes
    a simple API for reading/updating attribute `a`.
    """

    _instances: dict = {}  # Class-level dict for instances (keyed by cls for generality)
    _lock: threading.Lock = threading.Lock()  # For thread-safety

    def __new__(cls, *args, **kwargs):
        # Double-checked locking for thread-safety
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    # Create the instance
                    instance = super().__new__(cls)
                    # Manually initialize ONLY on creation
                    instance.__init__(*args, **kwargs)
                    cls._instances[cls] = instance
                    logger.info("Created new instance of %s", cls.__name__)
                    return instance
        else:
            logger.debug("Returning existing instance of %s", cls.__name__)
        return cls._instances[cls]

    def __init__(self, *args, **kwargs):
        # This now runs ONLY on first creation (guarded by __new__)
        # default value for `a` can be overridden via keyword argument
        self.a = kwargs.pop("a", 90)
        self.args = args
        self.kwargs = kwargs
        logger.debug(
            "Initialized %s with a=%s args=%s kwargs=%s",
            self.__class__.__name__,
            self.a,
            self.args,
            self.kwargs,
        )

    def printing(self) -> int:
        """Example method that returns a constant value.

        Kept from original code for compatibility with existing callers.
        """
        return 1

    def setting(self, value: int = 100) -> None:
        """Set attribute `a` to a new integer value."""
        self.a = value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} a={self.a} args={self.args} kwargs={self.kwargs}>"


class ObjWithoutSingleton:
    """A regular (non-singleton) class with the same public API as `Obj`."""

    def __init__(self, *args, **kwargs):
        self.a = kwargs.pop("a", 90)
        self.args = args
        self.kwargs = kwargs
        logger.debug(
            "Initialized %s with a=%s args=%s kwargs=%s",
            self.__class__.__name__,
            self.a,
            self.args,
            self.kwargs,
        )

    def printing(self) -> int:
        return 1

    def setting(self, value: int = 100) -> None:
        self.a = value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} a={self.a} args={self.args} kwargs={self.kwargs}>"


if __name__ == "__main__":
    # Small demonstration showing singleton vs non-singleton behavior
    s = Obj(1, 2, 3)
    d = Obj(4, 5, 6)

    # s and d should be the same instance
    logger.info("s is d: %s", s is d)
    logger.info("s: %s d: %s", s, d)

    g = ObjWithoutSingleton(1, 2, 3)
    h = ObjWithoutSingleton(8, 7, 6)

    # g and h should be different instances
    logger.info("g is h: %s", g is h)
    logger.info("g: %s h: %s", g, h)

    logger.info("printing(): %s", s.printing())

    # demonstrate setting values
    s.setting()
    g.setting()

    logger.info("After setting: s.a=%s, d.a=%s", s.a, d.a)
    logger.info("After setting: g.a=%s, h.a=%s", g.a, h.a)