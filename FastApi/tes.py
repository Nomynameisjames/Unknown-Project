#!/usr/bin/env python3
import asyncio
from asyncio import get_running_loop
import time

async def count(delay: int):
    await asyncio.sleep(4)
    if delay == 3:
        raise asyncio.CancelledError('delay can not be 3')
    await asyncio.sleep(delay)
    print("counting...")
    return f"done"

async def errcount(delay: int):
    if not isinstance(delay, int):
        raise asyncio.CancelledError("delay must be int")
    await asyncio.sleep(delay)
    print("errcounting...")

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            #await asyncio.sleep(5)
            async with asyncio.timeout(None) as cm:
                loop = get_running_loop().time() + 10
                print(loop)
                cm.reschedule(loop)
                task_3 = tg.create_task(count(3))
                task_1 = tg.create_task(count(1))
                task_2 = tg.create_task(errcount(2))
                print(f"started at {time.strftime('%X')}")
                await asyncio.sleep(30)
                await task_1
                await task_2
                print(f"all tasks are now completed {task_1.result()} {task_2.result()}")
    except TimeoutError:
        print("The long operation timed out, but we've handled it.")
    except Exception as e:
        if isinstance(e, ExceptionGroup):
            for sub_exception in e.exceptions:
                print(f"Sub-exception caught: {sub_exception}")
        print(f"Exception caught .... {e}")
    finally:
        print(f"ended at: {time.strftime('%X')}")

async def main_2():
#    background_task = set()
    try:
        for i in range(10):
            done, task = await asyncio.wait(count(i))
        # print(f"awaitable object {task}\n")
        #background_task.add(task)
            print(task)
    except TimeoutError as e:
        print(f" timeout {e}")
    except asyncio.CancelledError as e:
        print(f"the following error occured {e}")
      #  print(f"background_task {background_task}\n")
       # task.add_done_callback(background_task.discard)
       # print(f"background_task {background_task}\n")




if __name__ == "__main__":
    asyncio.run(main_2())
