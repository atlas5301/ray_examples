import ray
import os
import time

@ray.remote
def f():
    print("hey!!!")
    time.sleep(1)
    print("remote: current path is: ", os.getcwd())
    time.sleep(1)
    return

if __name__ == "__main__":
    ray.init()
    print("local: current path is: ", os.getcwd())
    ray.get(f.remote())
    ray.shutdown()