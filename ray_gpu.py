import ray
import os

ray.init()

@ray.remote(num_gpus=1)
def print_cuda_env():
    return os.environ.get("CUDA_VISIBLE_DEVICES")

# Call the remote function
future = print_cuda_env.remote()

# Get the result
result = ray.get(future)
print(result)  # prints the CUDA_VISIBLE_DEVICES or a message if it's not set

ray.shutdown()