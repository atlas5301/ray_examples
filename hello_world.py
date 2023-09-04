import ray

@ray.remote
def hello_world(x):
    import time
    print(time.time())
    time.sleep(1)
    print(f"hello_world: {x}")
    return x * x

if __name__ == '__main__':
    ray.init()
    id = hello_world.remote(0)
    print(type(id), id)
    result = ray.get(id)
    print(type(result), result)
    print("---------------------------------")
    ids = [hello_world.remote(i) for i in range(3)]
    ray.get(ids)
    print("---------------------------------")
    for i in range(3):
        ray.get(hello_world.remote(i))
    ray.shutdown()



