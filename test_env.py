import os
import ray

runtime_env = {
    'env_vars': {'ENV_VAR_1': 'env_var_value'}
}

# Actors

@ray.remote(runtime_env=runtime_env)
class Actor:
    def method(self):
        print(os.environ['ENV_VAR_1'])

a = Actor.remote()
ray.get(a.method.remote())

# Tasks

@ray.remote(runtime_env=runtime_env)
def f():
    print(os.environ['ENV_VAR_1'])

ray.get(f.remote())