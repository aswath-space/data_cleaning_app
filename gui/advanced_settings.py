from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QTextEdit, QMessageBox
import json
from config import config  # Import the shared config dictionary

# Placeholder for CustomModel. This should be replaced by user-defined code.
class CustomModel:
    def fit(self, X, y=None):
        pass

    def predict(self, X):
        pass

    def set_params(self, **params):
        pass

class AdvancedSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Advanced Settings')
        
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.model_label = QLabel('Custom Model (Python code):')
        self.model_input = QTextEdit()  # Use QTextEdit for larger code input area
        form_layout.addRow(self.model_label, self.model_input)
        
        self.param_label = QLabel('Model Parameters (JSON):')
        self.param_input = QLineEdit()
        form_layout.addRow(self.param_label, self.param_input)
        
        layout.addLayout(form_layout)
        
        self.save_button = QPushButton('Save Settings')
        self.save_button.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)
        
    def save_settings(self):
        custom_model_code = self.model_input.toPlainText()  # Get text from QTextEdit
        model_parameters_json = self.param_input.text()
        
        try:
            model_parameters = json.loads(model_parameters_json)
            # Validate and store the custom model and parameters
            exec(custom_model_code)
            custom_model = CustomModel()
            custom_model.set_params(**model_parameters)
            
            # Store the custom model and parameters in a configuration object
            config['custom_model'] = custom_model
            config['custom_model_code'] = custom_model_code
            config['model_parameters'] = model_parameters
            
            QMessageBox.information(self, 'Settings Saved', 'Your advanced settings have been saved successfully.')
            self.accept()
        except json.JSONDecodeError:
            QMessageBox.critical(self, 'Error', 'Invalid JSON format for model parameters.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error in custom model code: {e}')
