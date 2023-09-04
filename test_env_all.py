import os
import ray

runtime_env = {
    'env_vars': {'ENV_VAR_1': 'env_var_value'}
}

# Actors

@ray.remote
class Actor:
    def method(self):
        print(os.environ['ENV_VAR_1'])

# Tasks

@ray.remote
def f():
    print(os.environ['ENV_VAR_1'])

ray.init(runtime_env=runtime_env)

a = Actor.remote()
ray.get(a.method.remote())

ray.get(f.remote())

ray.shutdown()