import controlflow as cf


@cf.flow
def height_flow(poem_topic: str):
    height = cf.Task(
        "Get the user's height",
        user_access=True,
        result_type=int,
        instructions="convert the height to inches",
    )
    height.run()

    if height.result < 40:
        raise ValueError("You must be at least 40 inches tall to receive a poem")
    else:
        return cf.Task(
            "Write a poem for the user that takes their height into account",
            context=dict(height=height, topic=poem_topic),
        )


height_flow(poem_topic="flowers and keep the poem short")
