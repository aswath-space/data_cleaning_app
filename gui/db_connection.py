from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout, QComboBox, QMessageBox
from database.connection import get_engine, test_connection

class DbConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Database Connection')
        
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        # Database Type Selection
        self.db_type_label = QLabel('Database Type:')
        self.db_type_input = QComboBox()
        self.db_type_input.addItems(['sqlite', 'postgresql', 'mysql', 'mssql', 'oracle'])
        form_layout.addRow(self.db_type_label, self.db_type_input)
        
        # Host Input
        self.host_label = QLabel('Host:')
        self.host_input = QLineEdit()
        form_layout.addRow(self.host_label, self.host_input)
        
        # Port Input
        self.port_label = QLabel('Port:')
        self.port_input = QLineEdit()
        form_layout.addRow(self.port_label, self.port_input)
        
        # Username Input
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        form_layout.addRow(self.username_label, self.username_input)
        
        # Password Input
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(self.password_label, self.password_input)
        
        # Database Name Input
        self.db_name_label = QLabel('Database Name:')
        self.db_name_input = QLineEdit()
        form_layout.addRow(self.db_name_label, self.db_name_input)
        
        layout.addLayout(form_layout)
        
        # Connect Button
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.connect_to_database)
        layout.addWidget(self.connect_button)
        
        self.setLayout(layout)
    
    def connect_to_database(self):
        """
        Connect to the database using the provided details.
        """
        db_type = self.db_type_input.currentText()
        host = self.host_input.text()
        port = self.port_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        db_name = self.db_name_input.text()
        
        # Create the database engine
        engine = get_engine(db_type, host, port, username, password, db_name)
        
        # Test the connection and show a message box with the result
        if test_connection(engine):
            QMessageBox.information(self, 'Connection Successful', 'Successfully connected to the database.')
            self.accept()
        else:
            QMessageBox.critical(self, 'Connection Failed', 'Failed to connect to the database. Please check your details and try again.')
