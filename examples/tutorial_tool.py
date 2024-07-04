import controlflow as cf
import random


def roll_die(n: int) -> int:
    """Roll an n-sided die"""
    return random.randint(1, n)


task = cf.Task(
    "Roll 5 dice, three with 6 sides and two with 20 sides. the 20 side die has numbers 1-20 - run the die with 20 sides last",
    tools=[roll_die],
    result_type=list[int],
)


task.run()

print(task.result)
