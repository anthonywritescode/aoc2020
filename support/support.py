import contextlib
import time
from typing import Generator


@contextlib.contextmanager
def timing(name: str = '') -> Generator[None, None, None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = 'ms'
        if t < 100:
            t *= 1000
            unit = 'μs'
        if name:
            name = f' ({name})'
        print(f'> {int(t)} {unit}{name}')
