from unittest import TestCase
from modules.logger import create_logger


class TestLogger(TestCase):

    def setUp(self) -> None:
        self._test_logger = create_logger(logger_name='test_logger',
                                          logging_level='debug')

    def test_logger(self):
        with self.assertLogs('test_logger', level="DEBUG") as cm:
            self._test_logger.debug("Testing 123")
            self._test_logger.info("This is info")
            self.assertEqual(cm.output,
                     ['DEBUG:test_logger:Testing 123','INFO:test_logger:This is info'])
