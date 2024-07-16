import unittest
from unittest.mock import patch, call
from ansible_inventory_logger import InventoryLogger  # Ensure the import path is correct
import logging
from globals import MIN_LOG_LEVEL  # Import the minimum log level from globals

class TestInventoryLogger(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Reset the logger before each test to ensure clean state
        self.logger = InventoryLogger()

    @patch('ansible_inventory_logger.EXIT_ON_FATAL', False)
    @patch('ansible_inventory_logger.EXIT_ON_ERROR', False)
    @patch('ansible_inventory_logger.logging.Logger.addHandler')
    def test_handler_setup(self, mock_add_handler):
        """Ensure that handlers are added based on configuration."""
        logger = InventoryLogger()
        self.assertTrue(mock_add_handler.called)

    ## ToDO - Test Broken.
    # @patch('logging.StreamHandler.emit')
    # def test_logging_output(self, mock_emit):
    #     """Test output to console depending on the log level."""
    #     logger = InventoryLogger(level=logging.INFO)
    #     logger.warning("Test warning")
    #     mock_emit.assert_called_once()  # Ensures that warnings and above are logged

    @patch('ansible_inventory_logger.logging.Logger.log')
    def test_custom_log_format(self, mock_log):
        """Test custom log formatting."""
        with patch('ansible_inventory_logger.sys.exit'):
            logger = InventoryLogger()
            logger.debug("Debug message")
            args, kwargs = mock_log.call_args
            self.assertIn("Debug message", args[1])  # Custom formatting inclusion

    @patch('ansible_inventory_logger.sys.exit')
    def test_exit_on_fatal(self, mock_exit):
        """Ensure fatal logs trigger an exit."""
        logger = InventoryLogger()
        with patch('ansible_inventory_logger.EXIT_ON_FATAL', True):
            logger.fatal("Fatal error")
            mock_exit.assert_called_once()

    # @patch('ansible_inventory_logger.RotatingFileHandler.doRollover')
    # @patch('ansible_inventory_logger.logging.handlers.RotatingFileHandler.emit')
    # def test_file_logging_and_rotation(self, mock_emit, mock_rollover):
    #     """Test file logging and log rotation behavior."""
    #     with patch('ansible_inventory_logger.ENABLE_FILE_LOGGING', True), \
    #          patch('ansible_inventory_logger.ENABLE_LOG_ROTATION', True):
    #         logger = InventoryLogger()
    #         logger.error("Error message that triggers log rotation")
            
    #         # Directly trigger the rollover
    #         logger.logger.handlers[1].doRollover()
            
    #         self.assertEqual(mock_emit.call_count, 1)
    #         mock_rollover.assert_called_once()  # Ensure rotation is triggered on conditions

    ## ToDo - Fix this test too.
    # @patch('ansible_inventory_logger.EXIT_ON_FATAL', False)
    # @patch('ansible_inventory_logger.EXIT_ON_ERROR', False)
    # @patch('logging.Logger.log')
    # def test_log_level_effectiveness(self, mock_log):
    #     """Test if logger respects different log levels."""
    #     log_levels = [
    #         logging.DEBUG,
    #         logging.INFO,
    #         logging.WARNING,
    #         logging.ERROR,
    #         logging.CRITICAL
    #     ]

    #     for level in log_levels:
    #         with self.subTest(level=level):
    #             logger = InventoryLogger(level=level)
                
    #             # Reset mock call count for each level test
    #             mock_log.reset_mock()
                
    #             logger.debug("Debug message")
    #             logger.info("Info message")
    #             logger.warning("Warning message")
    #             logger.error("Error message")
    #             logger.critical("Critical message")

    #             # Get current module and method names
    #             current_frame = inspect.currentframe()
    #             module_name = current_frame.f_globals['__name__']
    #             method_name = current_frame.f_code.co_name

    #             # Expected messages with custom formatting
    #             expected_calls = [call(call_level, f"{module_name} {method_name}: {message}") for call_level, message in [
    #                 (logging.DEBUG, "Debug message"),
    #                 (logging.INFO, "Info message"),
    #                 (logging.WARNING, "Warning message"),
    #                 (logging.ERROR, "Error message"),
    #                 (logging.CRITICAL, "Critical message")
    #             ] if call_level >= level]

    #             self.assertEqual(mock_log.call_count, len(expected_calls))
                
    #             # Verify that each expected call was made
    #             actual_calls = [(args[0], args[1]) for args, _ in mock_log.call_args_list]
    #             self.assertEqual(actual_calls, expected_calls)

if __name__ == '__main__':
    unittest.main()
