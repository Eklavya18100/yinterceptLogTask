import asyncio
from log_component import LogComponent


async def main():
    asyncio.create_task(log_component._process_queue())
    await log_component.queue.join()


if __name__ == "__main__":

    log_component = LogComponent()
    # Start processing the log messages
    log_component.write("Log message 1")
    log_component.write("Log message 2")

    asyncio.run(main())
    # log_component.stop(immediate=False)
    # log_component.wait_for_completion()
    # loop.run_until_complete(log_component.stop(immediate=True))  # Stop processing the queue immediately
    # loop.close()