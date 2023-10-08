import unittest
import asyncio
import datetime
from unittest.mock import patch
from async_logger.log_component import LogComponent

class LogComponentTestCase(unittest.TestCase):
    def setUp(self):
        self.log_component = LogComponent()

    def tearDown(self):
        self.log_component.stop(immediate=True)

    async def wait_for_completion(self):
        await self.log_component.wait_for_completion()

    async def get_log_file_content(self, filename):
        with open(filename, 'r') as log_file:
            return log_file.read()

    @patch('asyncio.sleep', return_value=None)
    @patch('asyncio.get_event_loop')
    def test_call_to_Ilog_writes_something(self, mock_get_event_loop, mock_sleep):
        log_message = "Log message"
        expected_content = log_message + "\n"

        mock_loop = asyncio.new_event_loop()
        mock_get_event_loop.return_value = mock_loop

        mock_loop.run_until_complete(self.log_component.write(log_message))
        mock_loop.run_until_complete(asyncio.gather(self.wait_for_completion()))

        log_file_content = mock_loop.run_until_complete(
            self.get_log_file_content(self.log_component.current_log_file)
        )

        self.assertEqual(log_file_content, expected_content)

    @patch('asyncio.sleep', return_value=None)
    @patch('asyncio.get_event_loop')
    def test_new_files_created_if_midnight_crossed(self, mock_get_event_loop, mock_sleep):
        now = datetime.datetime.now()
        today = now.strftime('%Y_%m_%d')
        yesterday = (now - datetime.timedelta(days=1)).strftime('%Y_%m_%d')

        mock_loop = asyncio.new_event_loop()
        mock_get_event_loop.return_value = mock_loop

        # Write a log message on the current day
        mock_loop.run_until_complete(self.log_component.write("Log message"))
        mock_loop.run_until_complete(asyncio.gather(self.wait_for_completion()))

        # Check if the log file is created with today's date
        self.assertEqual(self.log_component.current_log_file, f"log_{today}.txt")

        # Move the time to the next day
        mock_loop.call_later(1, mock_loop.stop)
        mock_loop.run_forever()

        # Write a log message on the next day
        mock_loop.run_until_complete(self.log_component.write("Log message"))
        mock_loop.run_until_complete(asyncio.gather(self.wait_for_completion()))

        # Check if a new log file is created with the new date
        self.assertEqual(self.log_component.current_log_file, f"log_{yesterday}.txt")

    @patch('asyncio.sleep', return_value=None)
    @patch('asyncio.get_event_loop')
    def test_stop_behavior(self, mock_get_event_loop, mock_sleep):
        log_messages = ["Log message 1", "Log message 2", "Log message 3"]

        mock_loop = asyncio.new_event_loop()
        mock_get_event_loop.return_value = mock_loop

        # Write log messages
        for message in log_messages:
            mock_loop.run_until_complete(self.log_component.write(message))

        mock_loop.call_later(1, mock_loop.stop)
        mock_loop.run_forever()

        # Stop processing immediately
        self.log_component.stop(immediate=True)

        # Check if the queue is empty
        self.assertTrue(self.log_component.queue.empty())

        # Stop processing with completion
        self.log_component.stop(immediate=False)

        # Check if the queue is empty after waiting for completion
        mock_loop.run_until_complete(asyncio.gather(self.wait_for_completion()))
        self.assertTrue(self.log_component.queue.empty())

if __name__ == "__main__":
    unittest.main()