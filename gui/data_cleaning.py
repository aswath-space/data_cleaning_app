from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout, QComboBox, QMessageBox
import pandas as pd
from data_cleaning.cleaning_functions import (handle_missing_values, remove_duplicates, 
                                              convert_dtypes, knn_impute, iterative_impute, 
                                              winsorize_data, robust_scale, parse_dates, 
                                              extract_date_features, fill_missing_timestamps, 
                                              smooth_time_series, remove_outliers, normalize_data,
                                              encode_categorical, scale_features, handle_imbalanced_data,
                                              log_transform, create_cluster_features, automated_feature_engineering)
from data_cleaning.text_cleaning import (tokenize_text_nltk, tokenize_text_sklearn, stem_text, lemmatize_text, 
                                         remove_stopwords, normalize_text, named_entity_recognition, 
                                         sentiment_analysis, tfidf_vectorization)
from data_cleaning.anomaly_detection import (detect_anomalies_pycaret, detect_anomalies_pyod, 
                                             detect_anomalies_isolation_forest, detect_anomalies_autoencoder, 
                                             detect_anomalies_lstm)


class DataCleaningDialog(QDialog):
    def __init__(self, parent=None, df=None):
        super().__init__(parent)
        self.setWindowTitle('Data Cleaning')
        self.df = df

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.strategy_label = QLabel('Missing Values Strategy:')
        self.strategy_input = QComboBox()
        self.strategy_input.addItems(['mean', 'median', 'most_frequent', 'constant', 'knn', 'iterative'])
        form_layout.addRow(self.strategy_label, self.strategy_input)

        self.columns_label = QLabel('Columns (comma separated):')
        self.columns_input = QLineEdit()
        form_layout.addRow(self.columns_label, self.columns_input)

        self.scale_label = QLabel('Scaling Method:')
        self.scale_input = QComboBox()
        self.scale_input.addItems(['standard', 'minmax', 'robust'])
        form_layout.addRow(self.scale_label, self.scale_input)

        self.encode_label = QLabel('Columns to Encode (comma separated):')
        self.encode_input = QLineEdit()
        form_layout.addRow(self.encode_label, self.encode_input)

        self.anomaly_label = QLabel('Anomaly Detection Method:')
        self.anomaly_input = QComboBox()
        self.anomaly_input.addItems(['None', 'PyCaret', 'PyOD', 'IsolationForest', 'Autoencoder', 'LSTM'])
        form_layout.addRow(self.anomaly_label, self.anomaly_input)

        self.date_label = QLabel('Date Columns (comma separated):')
        self.date_input = QLineEdit()
        form_layout.addRow(self.date_label, self.date_input)

        self.text_label = QLabel('Text Columns (comma separated):')
        self.text_input = QLineEdit()
        form_layout.addRow(self.text_label, self.text_input)

        layout.addLayout(form_layout)

        self.clean_button = QPushButton('Clean Data')
        self.clean_button.clicked.connect(self.clean_data)
        layout.addWidget(self.clean_button)

        self.setLayout(layout)

    def clean_data(self):
        strategy = self.strategy_input.currentText()
        columns = self.columns_input.text().split(',')

        # Handle missing values
        if strategy in ['mean', 'median', 'most_frequent', 'constant']:
            self.df = handle_missing_values(self.df, strategy, columns)
        elif strategy == 'knn':
            self.df = knn_impute(self.df, columns)
        elif strategy == 'iterative':
            self.df = iterative_impute(self.df, columns)
        
        self.df = remove_duplicates(self.df)

        # Scale features
        scale_method = self.scale_input.currentText()
        if scale_method == 'standard':
            self.df = scale_features(self.df, columns)
        elif scale_method == 'minmax':
            self.df = normalize_data(self.df, columns)
        elif scale_method == 'robust':
            self.df = robust_scale(self.df, columns)

        # Encode categorical features
        encode_columns = self.encode_input.text().split(',')
        if encode_columns:
            self.df = encode_categorical(self.df, encode_columns)

        # Anomaly detection
        anomaly_method = self.anomaly_input.currentText()
        if anomaly_method == 'PyCaret':
            self.df = detect_anomalies_pycaret(self.df, columns)
        elif anomaly_method == 'PyOD':
            self.df = detect_anomalies_pyod(self.df, columns)
        elif anomaly_method == 'IsolationForest':
            self.df = detect_anomalies_isolation_forest(self.df, columns)
        elif anomaly_method == 'Autoencoder':
            self.df = detect_anomalies_autoencoder(self.df, columns)
        elif anomaly_method == 'LSTM':
            self.df = detect_anomalies_lstm(self.df, columns)

        # Date features extraction
        date_columns = self.date_input.text().split(',')
        for column in date_columns:
            self.df = parse_dates(self.df, [column])
            self.df = extract_date_features(self.df, column)

        # Text processing
        text_columns = self.text_input.text().split(',')
        for column in text_columns:
            self.df = tokenize_text_nltk(self.df, column)
            self.df = stem_text(self.df, column)
            self.df = lemmatize_text(self.df, column)
            self.df = remove_stopwords(self.df, column)
            self.df = normalize_text(self.df, column)
            self.df = named_entity_recognition(self.df, column)
            self.df = sentiment_analysis(self.df, column)
            # Additional: TF-IDF vectorization can be handled separately due to its output format

        QMessageBox.information(self, 'Data Cleaning', 'Data cleaning completed successfully!')
        self.accept()
