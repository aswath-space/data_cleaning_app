import unittest
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from gui.main_window import MainWindow
from unittest.mock import patch, MagicMock

class TestGUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.window = MainWindow()

    def test_window_title(self):
        self.assertEqual(self.window.windowTitle(), 'Data Cleaning Tool', "Window title mismatch")

    def test_db_button_enabled(self):
        self.assertTrue(self.window.db_button.isEnabled(), "DB button should be enabled initially")

    def test_clean_button_disabled(self):
        self.assertFalse(self.window.clean_button.isEnabled(), "Clean button should be disabled initially")

    def test_visualize_button_disabled(self):
        self.assertFalse(self.window.visualize_button.isEnabled(), "Visualize button should be disabled initially")

    def test_sql_button_disabled(self):
        self.assertFalse(self.window.sql_button.isEnabled(), "SQL button should be disabled initially")

    @patch('gui.main_window.get_engine')
    @patch('gui.main_window.test_connection')
    def test_db_connection_success(self, mock_test_connection, mock_get_engine):
        mock_test_connection.return_value = True
        mock_get_engine.return_value = MagicMock()

        # Simulate user input
        with patch('gui.db_connection.QDialog.exec_', return_value=QDialog.Accepted):
            with patch('gui.db_connection.DbConnectionDialog.db_type_input', return_value=MagicMock(currentText=MagicMock(return_value='sqlite'))):
                with patch('gui.db_connection.DbConnectionDialog.host_input', return_value=MagicMock(text=MagicMock(return_value=''))):
                    with patch('gui.db_connection.DbConnectionDialog.port_input', return_value=MagicMock(text=MagicMock(return_value=''))):
                        with patch('gui.db_connection.DbConnectionDialog.username_input', return_value=MagicMock(text=MagicMock(return_value=''))):
                            with patch('gui.db_connection.DbConnectionDialog.password_input', return_value=MagicMock(text=MagicMock(return_value=''))):
                                with patch('gui.db_connection.DbConnectionDialog.db_name_input', return_value=MagicMock(text=MagicMock(return_value=':memory:'))):
                                    self.window.open_db_connection_dialog()

        self.assertTrue(self.window.clean_button.isEnabled(), "Clean button should be enabled after successful DB connection")
        self.assertTrue(self.window.visualize_button.isEnabled(), "Visualize button should be enabled after successful DB connection")
        self.assertTrue(self.window.sql_button.isEnabled(), "SQL button should be enabled after successful DB connection")

if __name__ == '__main__':
    unittest.main()
