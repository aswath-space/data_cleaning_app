import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from scipy.stats.mstats import winsorize
from sklearn.preprocessing import RobustScaler, MinMaxScaler, OneHotEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.cluster import KMeans
import featuretools as ft
import numpy as np

def handle_missing_values(df, strategy='mean', columns=None):
    """
    Handle missing values in the specified columns using the given strategy.
    Available strategies: 'mean', 'median', 'most_frequent', 'constant'.

    Parameters:
    df (pd.DataFrame): The dataframe.
    strategy (str): The imputation strategy.
    columns (list): List of columns to impute.

    Returns:
    pd.DataFrame: Dataframe with imputed values.
    """
    imputer = SimpleImputer(strategy=strategy)
    df[columns] = imputer.fit_transform(df[columns])
    return df

def remove_duplicates(df):
    """
    Remove duplicate rows from the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe.

    Returns:
    pd.DataFrame: Dataframe without duplicates.
    """
    return df.drop_duplicates()

def convert_dtypes(df, columns, dtype):
    """
    Convert data types of the specified columns.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to convert.
    dtype (type): The target data type.

    Returns:
    pd.DataFrame: Dataframe with converted data types.
    """
    df[columns] = df[columns].astype(dtype)
    return df

def knn_impute(df, columns, n_neighbors=5):
    """
    Impute missing values using K-Nearest Neighbors.
    This method uses the average value of the k-nearest neighbors to impute missing values.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to impute.
    n_neighbors (int): Number of neighbors to use for imputation.

    Returns:
    pd.DataFrame: Dataframe with imputed values.
    """
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df[columns] = imputer.fit_transform(df[columns])
    return df

def iterative_impute(df, columns):
    """
    Impute missing values using Iterative Imputer.
    This method models each feature with missing values as a function of other features and iteratively predicts missing values.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to impute.

    Returns:
    pd.DataFrame: Dataframe with imputed values.
    """
    imputer = IterativeImputer()
    df[columns] = imputer.fit_transform(df[columns])
    return df

def winsorize_data(df, columns, limits):
    """
    Apply Winsorization to limit extreme values in the specified columns.
    Winsorization limits extreme values to reduce the effect of possible outliers.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to winsorize.
    limits (tuple): Lower and upper bounds for winsorization.

    Returns:
    pd.DataFrame: Dataframe with winsorized values.
    """
    df[columns] = df[columns].apply(lambda x: winsorize(x, limits=limits))
    return df

def robust_scale(df, columns):
    """
    Scale features using RobustScaler to minimize the influence of outliers.
    This scaler removes the median and scales the data according to the interquartile range.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to scale.

    Returns:
    pd.DataFrame: Dataframe with scaled values.
    """
    scaler = RobustScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def parse_dates(df, columns):
    """
    Parse dates in the specified columns.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to parse as dates.

    Returns:
    pd.DataFrame: Dataframe with parsed dates.
    """
    for column in columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')
    return df

def extract_date_features(df, column):
    """
    Extract date features (year, month, day, dayofweek) from a date column.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The date column to extract features from.

    Returns:
    pd.DataFrame: Dataframe with extracted date features.
    """
    df[f'{column}_year'] = df[column].dt.year
    df[f'{column}_month'] = df[column].dt.month
    df[f'{column}_day'] = df[column].dt.day
    df[f'{column}_dayofweek'] = df[column].dt.dayofweek
    return df

def fill_missing_timestamps(df, date_column, freq='D'):
    """
    Fill missing timestamps in a time series dataframe.
    This method resamples the dataframe to fill missing timestamps based on a specified frequency.

    Parameters:
    df (pd.DataFrame): The dataframe.
    date_column (str): The date column to resample.
    freq (str): The frequency for resampling.

    Returns:
    pd.DataFrame: Dataframe with missing timestamps filled.
    """
    df.set_index(date_column, inplace=True)
    df = df.resample(freq).asfreq()
    df.reset_index(inplace=True)
    return df

def smooth_time_series(df, column, window_size):
    """
    Smooth time series data using a rolling mean.
    This method reduces noise in the data by averaging data points within a specified window.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column to smooth.
    window_size (int): The window size for rolling mean.

    Returns:
    pd.DataFrame: Dataframe with smoothed time series.
    """
    df[column] = df[column].rolling(window=window_size).mean()
    return df

def remove_outliers(df, columns):
    """
    Remove outliers using the IQR method.
    This method uses the interquartile range to identify and remove outliers.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to check for outliers.

    Returns:
    pd.DataFrame: Dataframe with outliers removed.
    """
    Q1 = df[columns].quantile(0.25)
    Q3 = df[columns].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[~((df[columns] < lower_bound) | (df[columns] > upper_bound)).any(axis=1)]
    return df

def normalize_data(df, columns):
    """
    Normalize data to the range [0, 1].
    This method scales each feature to a given range.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to normalize.

    Returns:
    pd.DataFrame: Dataframe with normalized values.
    """
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def encode_categorical(df, columns):
    """
    Encode categorical variables using one-hot encoding.
    This method converts categorical variables into a form that can be provided to machine learning algorithms to do a better job in prediction.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of categorical columns to encode.

    Returns:
    pd.DataFrame: Dataframe with encoded categorical variables.
    """
    encoder = OneHotEncoder(sparse=False, drop='first')
    encoded_df = pd.DataFrame(encoder.fit_transform(df[columns]), columns=encoder.get_feature_names_out(columns))
    df = df.drop(columns, axis=1)
    df = pd.concat([df, encoded_df], axis=1)
    return df

def scale_features(df, columns):
    """
    Scale features to have zero mean and unit variance.
    This method standardizes the features.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to scale.

    Returns:
    pd.DataFrame: Dataframe with scaled features.
    """
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def handle_imbalanced_data(X, y):
    """
    Handle imbalanced data using SMOTE (Synthetic Minority Over-sampling Technique).
    This method balances the dataset by oversampling the minority class.

    Parameters:
    X (pd.DataFrame): Feature dataframe.
    y (pd.Series): Target series.

    Returns:
    pd.DataFrame, pd.Series: Resampled feature and target dataframes.
    """
    smote = SMOTE()
    X_res, y_res = smote.fit_resample(X, y)
    return X_res, y_res

def log_transform(df, columns):
    """
    Apply log transformation to specified columns.
    This method transforms the data to reduce skewness.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to transform.

    Returns:
    pd.DataFrame: Dataframe with log-transformed columns.
    """
    df[columns] = df[columns].apply(lambda x: np.log1p(x))
    return df

def create_cluster_features(df, columns, n_clusters=5):
    """
    Create cluster-based features using KMeans clustering.
    This method applies the KMeans clustering algorithm to the specified columns,
    assigns each data point to a cluster, and adds a new column with the cluster labels.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to use for clustering.
    n_clusters (int): Number of clusters.

    Returns:
    pd.DataFrame: Dataframe with an additional column 'cluster' indicating cluster assignments.
    """
    kmeans = KMeans(n_clusters=n_clusters)
    clusters = kmeans.fit_predict(df[columns])
    df['cluster'] = clusters
    return df

def automated_feature_engineering(df, target_column):
    """
    Perform automated feature engineering using Featuretools.
    This method creates an entity set from the dataframe, automatically generates
    new features, and returns a feature matrix with the new features.

    Parameters:
    df (pd.DataFrame): The dataframe.
    target_column (str): The target column for feature engineering.

    Returns:
    pd.DataFrame: Dataframe with automatically generated features.
    """
    es = ft.EntitySet(id='data')
    es.entity_from_dataframe(entity_id='df', dataframe=df, index='index')
    feature_matrix, feature_defs = ft.dfs(entityset=es, target_entity='df')
    return feature_matrix
