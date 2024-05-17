from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QDialog, QInputDialog, QSizePolicy
from PySide6.QtGui import QFont, QIcon
from database.connection import get_engine, test_connection
from database.fetch_data import fetch_data
from gui.sql_query_builder import SQLQueryBuilderDialog
from gui.advanced_settings import AdvancedSettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Cleaning Tool')
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout()
        
        header_label = QLabel('Welcome to the Data Cleaning Tool', self)
        header_label.setFont(QFont('Arial', 16, QFont.Bold))
        main_layout.addWidget(header_label)
        
        button_layout = QHBoxLayout()
        
        self.db_button = self.create_button('Connect to Database', 'icons/db_icon.png', self.open_db_connection_dialog)
        button_layout.addWidget(self.db_button)

        self.clean_button = self.create_button('Start Data Cleaning', 'icons/clean_icon.png', self.start_data_cleaning)
        self.clean_button.setEnabled(False)
        button_layout.addWidget(self.clean_button)

        self.visualize_button = self.create_button('Visualize Data', 'icons/visualize_icon.png', self.visualize_data)
        self.visualize_button.setEnabled(False)
        button_layout.addWidget(self.visualize_button)

        self.sql_button = self.create_button('SQL Query Builder', 'icons/sql_icon.png', self.open_sql_query_builder)
        self.sql_button.setEnabled(False)
        button_layout.addWidget(self.sql_button)

        self.advanced_button = self.create_button('Advanced Settings', 'icons/advanced_icon.png', self.open_advanced_settings)
        button_layout.addWidget(self.advanced_button)
        
        main_layout.addLayout(button_layout)
        self.central_widget.setLayout(main_layout)
        
        self.engine = None
        self.df = None

    def create_button(self, text, icon_path, callback):
        button = QPushButton(text, self)
        button.setIcon(QIcon(icon_path))
        button.setFont(QFont('Arial', 12))
        button.setStyleSheet("""
            QPushButton {
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            color: black;
            min-width: 150px;
            max-width: 200px;
            min-height: 40px;
            max-height: 50px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        """)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.clicked.connect(callback)
        return button



    def open_db_connection_dialog(self):
        from gui.db_connection import DbConnectionDialog
        dialog = DbConnectionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            db_type = dialog.db_type_input.currentText()
            host = dialog.host_input.text()
            port = dialog.port_input.text()
            username = dialog.username_input.text()
            password = dialog.password_input.text()
            db_name = dialog.db_name_input.text()
            
            self.engine = get_engine(db_type, host, port, username, password, db_name)
            
            if test_connection(self.engine):
                self.clean_button.setEnabled(True)
                self.visualize_button.setEnabled(True)
                self.sql_button.setEnabled(True)
                QMessageBox.information(self, 'Connection Successful', 'Successfully connected to the database.')
            else:
                self.clean_button.setEnabled(False)
                self.visualize_button.setEnabled(False)
                self.sql_button.setEnabled(False)
                QMessageBox.critical(self, 'Connection Failed', 'Failed to connect to the database.')

    def start_data_cleaning(self):
        table_name, ok = QInputDialog.getText(self, 'Table Name', 'Enter the table name:')
        if ok and table_name:
            self.df = fetch_data(self.engine, table_name)
            if self.df is not None:
                from gui.data_cleaning import DataCleaningDialog
                dialog = DataCleaningDialog(self, df=self.df)
                dialog.exec()
            else:
                QMessageBox.critical(self, 'Fetch Data', 'Failed to fetch data from the specified table.')

    def visualize_data(self):
        if self.df is None:
            QMessageBox.critical(self, 'No Data', 'Please fetch and clean the data first.')
            return
    
        viz_options = [
        'Scatter Plot (Plotly)', 'Line Plot (Plotly)', 'Histogram (Plotly)',
        'Bar Plot (Plotly)', 'Box Plot (Plotly)', 'Heatmap (Plotly)',
        'Scatter Plot (Bokeh)', 'Line Plot (Bokeh)', 'Histogram (Bokeh)',
        'Bar Plot (Bokeh)', 'Box Plot (Bokeh)', 'Heatmap (Bokeh)'
        ]

        icons = {
        'Scatter Plot (Plotly)': 'icons/scatter_plot_icon.png',
        'Line Plot (Plotly)': 'icons/line_plot_icon.png',
        'Histogram (Plotly)': 'icons/histogram_icon.png',
        'Bar Plot (Plotly)': 'icons/bar_plot_icon.png',
        'Box Plot (Plotly)': 'icons/box_plot_icon.png',
        'Heatmap (Plotly)': 'icons/heatmap_icon.png',
        'Scatter Plot (Bokeh)': 'icons/scatter_plot_icon.png',
        'Line Plot (Bokeh)': 'icons/line_plot_icon.png',
        'Histogram (Bokeh)': 'icons/histogram_icon.png',
        'Bar Plot (Bokeh)': 'icons/bar_plot_icon.png',
        'Box Plot (Bokeh)': 'icons/box_plot_icon.png',
        'Heatmap (Bokeh)': 'icons/heatmap_icon.png'
        }

        items = [(QIcon(icons[option]), option) for option in viz_options]
        viz_type, ok = QInputDialog.getItem(self, 'Visualization Type', 'Select the type of visualization:', items)
    
        if not ok:
            return
    
        # Get the X-axis column
        x_col, ok = QInputDialog.getText(self, 'X-Axis Column', 'Enter the column for the X-axis:')
        if not ok or not x_col:
            return

        # Determine if a Y-axis column is needed based on visualization type
        y_col = None
        if 'Scatter Plot' in viz_type or 'Line Plot' in viz_type or 'Bar Plot' in viz_type:
            y_col, ok = QInputDialog.getText(self, 'Y-Axis Column', 'Enter the column for the Y-axis:')
            if not ok or not y_col:
                return

        columns = [x_col] if not y_col else [x_col, y_col]

        from gui.visualization import (
        plot_scatter_plotly, plot_line_plotly, plot_histogram_plotly,
        plot_bar_plotly, plot_box_plotly, plot_heatmap_plotly,
        plot_scatter_bokeh, plot_line_bokeh, plot_histogram_bokeh,
        plot_bar_bokeh, plot_box_bokeh, plot_heatmap_bokeh
        )

        if viz_type == 'Scatter Plot (Plotly)':
            plot_scatter_plotly(self.df, x_col, y_col)
        elif viz_type == 'Line Plot (Plotly)':
            plot_line_plotly(self.df, x_col, y_col)
        elif viz_type == 'Histogram (Plotly)':
            plot_histogram_plotly(self.df, x_col)
        elif viz_type == 'Bar Plot (Plotly)':
            plot_bar_plotly(self.df, x_col, y_col)
        elif viz_type == 'Box Plot (Plotly)':
            plot_box_plotly(self.df, x_col)
        elif viz_type == 'Heatmap (Plotly)':
            plot_heatmap_plotly(self.df, columns)
        elif viz_type == 'Scatter Plot (Bokeh)':
            plot_scatter_bokeh(self.df, x_col, y_col)
        elif viz_type == 'Line Plot (Bokeh)':
            plot_line_bokeh(self.df, x_col, y_col)
        elif viz_type == 'Histogram (Bokeh)':
            plot_histogram_bokeh(self.df, x_col)
        elif viz_type == 'Bar Plot (Bokeh)':
            plot_bar_bokeh(self.df, x_col, y_col)
        elif viz_type == 'Box Plot (Bokeh)':
            plot_box_bokeh(self.df, x_col)
        elif viz_type == 'Heatmap (Bokeh)':
            plot_heatmap_bokeh(self.df, columns)


    def open_sql_query_builder(self):
        """
        Open the SQL Query Builder dialog.
        """
        if self.engine:
            dialog = SQLQueryBuilderDialog(self, engine=self.engine)
            dialog.exec()

    def open_advanced_settings(self):
        """
        Open the Advanced Settings dialog.
        """
        dialog = AdvancedSettingsDialog(self)
        dialog.exec()
