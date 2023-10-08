import os
import datetime
import asyncio
from ilog import ILog


class LogComponent(ILog):
    def __init__(self):
        self.current_log_file = None
        self.is_running = True
        self.queue = asyncio.Queue()

    async def write(self, message: str) -> None:
        if self.current_log_file is None or self._crossed_midnight():
            await self._create_new_log_file()

        await self.queue.put(message)

    async def stop(self, immediate: bool = False) -> None:
        self.is_running = False

        if not immediate:
            await self.wait_for_completion()

    async def wait_for_completion(self) -> None:
        await self.queue.join()

    def _crossed_midnight(self) -> bool:
        now = datetime.datetime.now()
        if self.current_log_file:
            log_file_creation_time = datetime.datetime.fromtimestamp(
                os.path.getctime(self.current_log_file)
            )
            return now.date() > log_file_creation_time.date()

        return False

    async def _create_new_log_file(self) -> None:
        now = datetime.datetime.now()
        filename = f"log_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        self.current_log_file = filename

        # Create a new log file
        with open(filename, 'w') as log_file:
            log_file.write(f"Log file created at {now}\n")

    async def _process_queue(self) -> None:
        while self.is_running or not self.queue.empty():
            message = await self.queue.get()
            try:
                with open(self.current_log_file, 'a') as log_file:
                    log_file.write(message + '\n')
            finally:
                self.queue.task_done()