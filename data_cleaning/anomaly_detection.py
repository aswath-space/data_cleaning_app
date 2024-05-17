from keras import layers, models
from pycaret.anomaly import setup, create_model, assign_model
from pyod.models.knn import KNN
from sklearn.ensemble import IsolationForest
import numpy as np
from config import config  # Import the shared config dictionary


def detect_anomalies_pycaret(df, columns):
    """
    Detect anomalies using PyCaret's anomaly detection module.
    This method sets up the environment, creates a KNN model, assigns anomalies, and returns the results.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to use for anomaly detection.

    Returns:
    pd.DataFrame: Dataframe with anomaly labels assigned.
    """
    s = setup(df[columns], silent=True, verbose=False)
    model = create_model('knn')
    results = assign_model(model)
    return results

def detect_anomalies_pyod(df, columns):
    """
    Detect anomalies using PyOD's KNN model.
    This method fits a KNN model and assigns anomaly labels to the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to use for anomaly detection.

    Returns:
    pd.DataFrame: Dataframe with anomaly labels assigned.
    """
    clf = KNN()
    clf.fit(df[columns])
    df['anomaly'] = clf.labels_
    return df

def detect_anomalies_isolation_forest(df, columns):
    """
    Detect anomalies using Isolation Forest.
    This method fits an Isolation Forest model and assigns anomaly labels to the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to use for anomaly detection.

    Returns:
    pd.DataFrame: Dataframe with anomaly labels assigned.
    """
    clf = IsolationForest(contamination=0.1)
    df['anomaly'] = clf.fit_predict(df[columns])
    return df

def build_autoencoder(input_dim):
    """
    Build an autoencoder model for anomaly detection.
    This method constructs an autoencoder with three layers in the encoder and decoder.

    Parameters:
    input_dim (int): The number of input features.

    Returns:
    keras.Model: Compiled autoencoder model.
    """
    input_layer = layers.Input(shape=(input_dim,))
    encoder = layers.Dense(64, activation='relu')(input_layer)
    encoder = layers.Dense(32, activation='relu')(encoder)
    encoder = layers.Dense(16, activation='relu')(encoder)
    decoder = layers.Dense(32, activation='relu')(encoder)
    decoder = layers.Dense(64, activation='relu')(decoder)
    decoder = layers.Dense(input_dim, activation='sigmoid')(decoder)
    autoencoder = models.Model(inputs=input_layer, outputs=decoder)
    autoencoder.compile(optimizer='adam', loss='mse')
    return autoencoder

def detect_anomalies_autoencoder(df, columns, epochs=50, batch_size=32):
    """
    Detect anomalies using an autoencoder.
    This method trains an autoencoder and uses reconstruction loss to identify anomalies.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to use for anomaly detection.
    epochs (int): Number of training epochs.
    batch_size (int): Batch size for training.

    Returns:
    pd.DataFrame: Dataframe with anomaly labels assigned based on reconstruction loss.
    """
    input_dim = len(columns)
    autoencoder = build_autoencoder(input_dim)
    autoencoder.fit(df[columns], df[columns], epochs=epochs, batch_size=batch_size, shuffle=True, validation_split=0.2, verbose=0)
    df['reconstruction_loss'] = autoencoder.evaluate(df[columns], df[columns], verbose=0)
    threshold = df['reconstruction_loss'].quantile(0.95)
    df['anomaly'] = df['reconstruction_loss'] > threshold
    return df

def build_lstm_autoencoder(input_shape):
    """
    Build an LSTM autoencoder model for time series anomaly detection.
    This method constructs an LSTM autoencoder with two LSTM layers in the encoder and decoder.

    Parameters:
    input_shape (tuple): Shape of the input data.

    Returns:
    keras.Model: Compiled LSTM autoencoder model.
    """
    model = models.Sequential()
    model.add(layers.LSTM(128, input_shape=input_shape, return_sequences=True))
    model.add(layers.LSTM(64, return_sequences=False))
    model.add(layers.RepeatVector(input_shape[0]))
    model.add(layers.LSTM(64, return_sequences=True))
    model.add(layers.LSTM(128, return_sequences=True))
    model.add(layers.TimeDistributed(layers.Dense(input_shape[1])))
    model.compile(optimizer='adam', loss='mae')
    return model

def detect_anomalies_lstm(df, column, time_steps=10, epochs=50, batch_size=32):
    """
    Detect anomalies in time series data using an LSTM autoencoder.
    This method trains an LSTM autoencoder and uses reconstruction loss to identify anomalies.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing the time series data.
    time_steps (int): Number of time steps for the LSTM.
    epochs (int): Number of training epochs.
    batch_size (int): Batch size for training.

    Returns:
    pd.DataFrame: Dataframe with anomaly labels assigned based on reconstruction loss.
    """
    data = df[column].values
    data = data.reshape((len(data), 1))

    X = []
    for i in range(time_steps, len(data)):
        X.append(data[i-time_steps:i, 0])

    X = np.array(X)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = build_lstm_autoencoder((time_steps, 1))
    model.fit(X, X, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=0)

    X_pred = model.predict(X)
    loss = np.mean(np.abs(X_pred - X), axis=1)

    df['reconstruction_loss'] = 0
    df['reconstruction_loss'].iloc[time_steps:] = loss
    threshold = df['reconstruction_loss'].quantile(0.95)
    df['anomaly'] = df['reconstruction_loss'] > threshold
    return df

def detect_anomalies_custom(df, columns):
    if 'custom_model' in config:
        custom_model = config['custom_model']
        custom_model.fit(df[columns])
        df['anomaly'] = custom_model.predict(df[columns])
    return df

def handle_anomalies(df, columns):
    if 'custom_model' in config:
        return detect_anomalies_custom(df, columns)
    else:
        return detect_anomalies_pycaret(df, columns)