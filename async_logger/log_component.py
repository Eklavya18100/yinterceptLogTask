import os
import datetime
import asyncio
from async_logger.ilog import ILog


class LogComponent(ILog):
    def __init__(self):
        self.current_log_file = None
        self.is_running = True
        self.queue = asyncio.Queue()
        now = datetime.datetime.now()
        self.last_date = now.strftime('%Y_%m_%d')
        os.makedirs('logs',exist_ok=True)
        self.last_filename = f"logs/{now.strftime('%Y_%m_%d_%H_%M_%S')}.txt"


    def write(self, message: str) -> None:
       self.queue.put_nowait(message)

    async def stop(self, immediate: bool = False) -> None:
        self.is_running = False

        if not immediate:
            await self.wait_for_completion()

    async def wait_for_completion(self) -> None:
        await self.queue.join()


    async def _create_new_log_file(self) -> None:
        now = datetime.datetime.now()
        filename = f"log_{now.strftime('%Y_%m_%d_%H_%M_%S')}.txt"
        self.current_log_file = filename

        # Create a new log file
        with open(filename, 'w') as log_file:
            log_file.write(f"Log file created at {now}\n")

    async def _process_queue(self) -> None:
        print('processing')
        while self.is_running or not self.queue.empty():
            message = await self.queue.get()

            # await self.handle(message)
            

            now = datetime.datetime.now()
            date_prefix = now.strftime('%Y_%m_%d')
            if date_prefix != self.last_date:
                self.last_date = date_prefix
                self.last_filename = f"logs/{now.strftime('%Y_%m_%d_%H_%M_%S')}.txt"

            try:
                with open(self.last_filename, 'a') as log_file:
                    log_file.write(message + '\n')
            finally:
                self.queue.task_done()