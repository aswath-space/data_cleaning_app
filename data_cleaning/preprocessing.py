import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, PolynomialFeatures, OneHotEncoder, KBinsDiscretizer

def scale_data(df, columns, method='standard'):
    """
    Scale data using either StandardScaler or MinMaxScaler.
    StandardScaler standardizes features by removing the mean and scaling to unit variance.
    MinMaxScaler transforms features by scaling each feature to a given range (default is 0 to 1).

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to scale.
    method (str): Scaling method - 'standard' or 'minmax'.

    Returns:
    pd.DataFrame: Dataframe with scaled columns.
    """
    scaler = StandardScaler() if method == 'standard' else MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def normalize_data(df, columns):
    """
    Normalize data to the range [0, 1] using MinMaxScaler.
    This is a convenience function that calls scale_data with method='minmax'.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to normalize.

    Returns:
    pd.DataFrame: Dataframe with normalized columns.
    """
    return scale_data(df, columns, method='minmax')

def encode_labels(df, columns):
    """
    Encode categorical labels with value between 0 and n_classes-1.
    This is useful for transforming non-numerical labels (as long as they are hashable and comparable) into numerical labels.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of categorical columns to encode.

    Returns:
    pd.DataFrame: Dataframe with encoded labels.
    """
    encoder = LabelEncoder()
    for column in columns:
        df[column] = encoder.fit_transform(df[column])
    return df

def create_polynomial_features(df, columns, degree=2):
    """
    Create polynomial features from the specified columns.
    This method generates polynomial and interaction features.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to transform.
    degree (int): The degree of the polynomial features.

    Returns:
    pd.DataFrame: Dataframe with original and polynomial features.
    """
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    poly_features = poly.fit_transform(df[columns])
    poly_df = pd.DataFrame(poly_features, columns=poly.get_feature_names_out(columns))
    df = pd.concat([df, poly_df], axis=1)
    return df

def one_hot_encode(df, columns):
    """
    Perform one-hot encoding on the specified categorical columns.
    One-hot encoding converts categorical variables into a form that can be provided to ML algorithms to do a better job in prediction.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of categorical columns to encode.

    Returns:
    pd.DataFrame: Dataframe with one-hot encoded columns.
    """
    encoder = OneHotEncoder(sparse=False, drop='first')
    encoded_df = pd.DataFrame(encoder.fit_transform(df[columns]), columns=encoder.get_feature_names_out(columns))
    df = df.drop(columns, axis=1)
    df = pd.concat([df, encoded_df], axis=1)
    return df

def create_interaction_features(df, columns):
    """
    Create interaction features from the specified columns.
    This method generates only interaction features (no polynomial features).

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to transform.

    Returns:
    pd.DataFrame: Dataframe with original and interaction features.
    """
    poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
    interaction_features = poly.fit_transform(df[columns])
    interaction_df = pd.DataFrame(interaction_features, columns=poly.get_feature_names_out(columns))
    df = pd.concat([df, interaction_df], axis=1)
    return df

def binning(df, columns, n_bins=5, encode='ordinal', strategy='uniform'):
    """
    Perform binning/discretization on the specified columns.
    This method converts continuous data into discrete bins.

    Parameters:
    df (pd.DataFrame): The dataframe.
    columns (list): List of columns to discretize.
    n_bins (int): Number of bins to produce.
    encode (str): The method used to encode the transformed result ('ordinal' or 'onehot').
    strategy (str): Strategy used to define the widths of the bins ('uniform', 'quantile', 'kmeans').

    Returns:
    pd.DataFrame: Dataframe with binned columns.
    """
    discretizer = KBinsDiscretizer(n_bins=n_bins, encode=encode, strategy=strategy)
    for column in columns:
        df[column + '_binned'] = discretizer.fit_transform(df[[column]])
    return df
