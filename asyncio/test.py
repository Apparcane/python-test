import asyncio
from contextvars import ContextVar

MyCounter = ContextVar('counter', default=0)


async def increase():
    my_counter = MyCounter.get()

    my_counter += 1

    MyCounter.set(my_counter)


async def count():
    while True:
        await increase()
        my_counter = MyCounter.get()
        print(f'Счетчик: {my_counter}')

        await asyncio.sleep(1 / 10)

asyncio.run(count())
