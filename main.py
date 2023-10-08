import asyncio
from log_component import LogComponent


async def main():
    log_component = LogComponent()
    await log_component.write("Log message 1")
    await log_component.write("Log message 2")
    await log_component.stop(immediate=False)
    await log_component.wait_for_completion()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    log_component = LogComponent()
    loop.create_task(log_component._process_queue())  # Start processing the log messages
    loop.run_until_complete(main())
    loop.run_until_complete(log_component.stop(immediate=True))  # Stop processing the queue immediately
    loop.close()