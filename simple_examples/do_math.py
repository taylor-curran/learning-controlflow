import random
import controlflow as cf


def do_math(n: int, n2: int):
    """Calculate the product"""
    return n * n2


task = cf.Task(
    "Multiple using 3 and 6",
    tools=[do_math],
    result_type=list[int],
)

task.run()
