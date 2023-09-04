import ray
from asyncio import Queue
import asyncio

ray.init()

@ray.remote
class test:
    def __init__(self):
        self.queue = Queue()
        for i in range(3):
            self.queue.put_nowait("hey")

    async def test(self, num):
        print(num)
        import time
        asyncio.sleep(0.5)
        return {'hello': 'hi'}
    
    def another_test(self):
        print("hey_again")

@ray.remote
class test2:
    def __init__(self, actor):
        self.actor = actor

    async def call_actor_method(self, method_name, *args, **kwargs):
        actor_method = getattr(self.actor, method_name)
        future = actor_method.remote(*args, **kwargs)
        return await asyncio.to_thread(ray.get, future)

class RayActorWrapper:
    def __init__(self, actor):
        self.actor = actor

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            return ray.get(self.actor.call_actor_method.remote(name, *args, **kwargs))
        return wrapper
    
def async_caller(object, queries):
    def process(q):
        return object.test(q)

    async def async_process(q):
        return await asyncio.to_thread(process, q)

    async def async_loop(datas):
        # This will start all process tasks concurrently and wait for all of them to finish
        results = await asyncio.gather(*(async_process(data) for data in datas))
        return results
    
    return asyncio.run(async_loop(queries))


test_base = test.remote()
ids = [test_base.test.remote(i) for i in range(5)]

ray.get(ids)

my_test = test2.remote(test_base)

wrapper = RayActorWrapper(my_test)
    
async_caller(wrapper, [i for i in range(10)])