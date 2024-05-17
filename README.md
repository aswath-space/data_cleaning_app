# My Advanced Data Cleaning Tool

This project is a comprehensive data cleaning tool designed to handle various data preprocessing tasks, anomaly detection, and visualization. The tool integrates multiple advanced libraries to provide a robust and user-friendly interface for data cleaning and analysis.

## Features

- Modern Desktop UI using PyQt/PySide
- Interactive Visualizations with Plotly, Bokeh, and Seaborn
- Multi-Database Support with SQLAlchemy, psycopg2, and PyMySQL
- Data Cleaning and Preprocessing with pandas, pyjanitor, and scikit-learn
- Anomaly Detection with PyCaret and PyOD
- Large-Scale Data Processing with Dask
- Data Validation with Cerberus
- Comprehensive Logging and Configuration Management

## Directory Structure

'''
my_advanced_data_cleaning_tool/
├── app.py
├── gui/
│ ├── init.py
│ ├── main_window.py
│ ├── db_connection.py
│ ├── data_cleaning.py
│ ├── sql_query_builder.py
│ ├── visualization.py
├── data_cleaning/
│ ├── init.py
│ ├── cleaning_functions.py
│ ├── anomaly_detection.py
│ ├── preprocessing.py
├── database/
│ ├── init.py
│ ├── connection.py
│ ├── fetch_data.py
│ ├── schema.py
├── utils/
│ ├── init.py
│ ├── file_operations.py
│ ├── config.py
│ ├── logging.py
├── tests/
│ ├── init.py
│ ├── test_cleaning_functions.py
│ ├── test_database.py
│ ├── test_gui.py
├── requirements.txt
├── README.md
└── LICENSE
'''

# Data Cleaning and Visualization Tool Instruction Manual
## Table of Contents
1. Introduction
2. Installation
3. Running the Application
4. User Interface Overview
5. Connecting to a Database
6. Data Cleaning
7. Visualization
8. SQL Query Builder
9. Testing

## Introduction
This tool provides a user-friendly interface for data cleaning and visualization. It supports connecting to various databases, cleaning data with advanced functions, visualizing data using Plotly and Bokeh, and building custom SQL queries.

## Installation
### Prerequisites
- Python 3.11 or 3.10
- Virtual Environment (optional but recommended)
### Steps
1. Clone the Repository:

'''
git clone <repository_url>
cd <repository_directory>
'''

2. Create and Activate a Virtual Environment:

'''
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
'''

3. Install Dependencies:

'''
pip install -r requirements.txt
'''

## Running the Application
To start the application, run:

'''
python data_cleaning_app/app.py
'''

## User Interface Overview
The main window of the application has several key components:
- Connect to Database: Opens a dialog to connect to a database.
- Start Data Cleaning: Opens the data cleaning dialog.
- Visualize Data: Opens the data visualization options.
- SQL Query Builder: Opens the SQL Query Builder dialog for custom queries.

## Connecting to a Database
1. Click the Connect to Database button.
2. Fill in the database details in the dialog:
    - Database Type: Select from 'sqlite', 'postgresql', 'mysql'.
    - Host: Enter the database host.
    - Port: Enter the database port.
    - Username: Enter the username.
    - Password: Enter the password.
    - Database Name: Enter the database name.
3. Click Connect. If the connection is successful, the other buttons will be enabled.

## Data Cleaning
1. Click the Start Data Cleaning button.
2. Enter the table name to fetch data from the connected database.
3. Use the following fields in the data cleaning dialog:
    - Missing Values Strategy: Choose the strategy for handling missing values.
    - Columns: Enter columns to apply the strategy to (comma-separated).
    - Scaling Method: Choose the method to scale the data.
    - Columns to Encode: Enter columns to encode (comma-separated).
    - Anomaly Detection Method: Choose the method for anomaly detection.
    - Date Columns: Enter date columns to parse (comma-separated).
    - Text Columns: Enter text columns to clean (comma-separated).
4. Click Clean Data. A message box will confirm the completion of the data cleaning.

## Visualization
1. Click the Visualize Data button.
2. Select the type of visualization from the dialog:
    - Scatter Plot
    - Line Plot
    - Histogram
    - Bar Plot
    - Box Plot
    - Heatmap
3. Enter the columns required for the selected visualization type.
4. The visualization will be displayed using Plotly or Bokeh.

## SQL Query Builder
1. Click the SQL Query Builder button.
2. Use the following fields in the SQL Query Builder dialog:
    - Select Fields: Enter the fields to select (comma-separated).
    - From Table: Enter the table name.
    - Conditions: Add conditions using the Add Condition button.
3. Click Execute Query to run the SQL query. The results will be displayed in the result output section.

## Testing
### unning Unit Tests
To run the unit tests, execute:

'''python -m unittest discover tests
'''

### GUI Testing
The test_gui.py file contains tests for the GUI components. Ensure the database connection and interaction tests are included.

## Additional Notes
- Configuration: Ensure the database details are correctly configured.
- Dependencies: Ensure all required Python packages are installed.
- Environment: Run the application in a virtual environment to avoid conflicts.

## Advanced Settings: Custom Model Integration

Our tool provides an Advanced Settings feature for integrating custom models and advanced configurations. This allows for greater flexibility and adaptability in data cleaning and anomaly detection processes.

### How to Use Advanced Settings

1. **Open Advanced Settings**:
   - Click on the **Advanced Settings** button in the main window.

2. **Input Custom Model Code**:
   - Enter your custom model code in the "Custom Model (Python code)" field.
   - Ensure your model class implements the required methods: `fit`, `predict`, and `set_params`.

3. **Specify Model Parameters**:
   - Enter model parameters in JSON format in the "Model Parameters (JSON)" field.

4. **Save Settings**:
   - Click **Save Settings** to validate and save your custom model and parameters.

5. **Run Data Cleaning**:
   - Continue with the data cleaning process. The tool will use your custom model during anomaly detection.

### Example

**Custom Model Code**:

```
class CustomModel:
    def fit(self, X, y=None):
        # Custom fitting logic
        pass

    def predict(self, X):
        # Custom prediction logic
        return [0 if x.mean() < 0.5 else 1 for x in X]

    def set_params(self, **params):
        # Custom parameter setting logic
        pass
# Model Parameters (JSON):
{
    "param1": 10,
    "param2": 0.01
}
'''