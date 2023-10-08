import asyncio
from async_logger.log_component import LogComponent


async def main():
    asyncio.create_task(log_component._process_queue())
    await log_component.queue.join()


if __name__ == "__main__":

    log_component = LogComponent()
    # Start processing the log messages
    log_component.write("Log message 1")
    log_component.write("Log message 2")

    asyncio.run(main())
   