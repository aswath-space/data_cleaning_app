import unittest
import pandas as pd
from data_cleaning.cleaning_functions import (handle_missing_values, remove_duplicates, 
                                              convert_dtypes, knn_impute, iterative_impute, 
                                              winsorize_data, robust_scale, parse_dates, 
                                              extract_date_features, fill_missing_timestamps, 
                                              smooth_time_series, remove_outliers, normalize_data,
                                              encode_categorical, scale_features, handle_imbalanced_data,
                                              log_transform, create_cluster_features, automated_feature_engineering)

class TestCleaningFunctions(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': [None, 2, 3, 4],
            'C': ['a', 'b', 'b', 'd'],
            'D': ['2021-01-01', '2021-01-02', None, '2021-01-04'],
            'E': [1, 2, 3, 4]
        })
        self.df['D'] = pd.to_datetime(self.df['D'])

    def test_handle_missing_values(self):
        result = handle_missing_values(self.df, strategy='mean', columns=['A', 'B'])
        self.assertAlmostEqual(result['A'].iloc[2], 2.3333333333333335, places=7, msg="Mean imputation failed")
        self.assertAlmostEqual(result['B'].iloc[0], 3.0, places=7, msg="Mean imputation failed")

    def test_remove_duplicates(self):
        result = remove_duplicates(self.df)
        self.assertEqual(len(result), 4, "Remove duplicates failed")

    def test_convert_dtypes(self):
        result = convert_dtypes(self.df, columns=['A'], dtype='float')
        self.assertEqual(result['A'].dtype, 'float64', "Convert dtypes failed")

    def test_knn_impute(self):
        result = knn_impute(self.df, columns=['A', 'B'])
        self.assertFalse(result.isnull().values.any(), "KNN imputation failed")

    def test_iterative_impute(self):
        result = iterative_impute(self.df, columns=['A', 'B'])
        self.assertFalse(result.isnull().values.any(), "Iterative imputation failed")

    def test_winsorize_data(self):
        result = winsorize_data(self.df, columns=['E'], limits=[0.1, 0.1])
        self.assertFalse(result['E'].isnull().values.any(), "Winsorization failed")

    def test_robust_scale(self):
        result = robust_scale(self.df, columns=['E'])
        self.assertAlmostEqual(result['E'].median(), 0.0, places=7, msg="Robust scaling failed")

    def test_parse_dates(self):
        result = parse_dates(self.df, columns=['D'])
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result['D']), "Parse dates failed")

    def test_extract_date_features(self):
        result = extract_date_features(self.df, 'D')
        self.assertIn('D_year', result.columns, "Extract date features failed")
        self.assertIn('D_month', result.columns, "Extract date features failed")
        self.assertIn('D_day', result.columns, "Extract date features failed")
        self.assertIn('D_dayofweek', result.columns, "Extract date features failed")

    def test_fill_missing_timestamps(self):
        result = fill_missing_timestamps(self.df, date_column='D', freq='D')
        self.assertFalse(result['D'].isnull().values.any(), "Fill missing timestamps failed")

    def test_smooth_time_series(self):
        result = smooth_time_series(self.df, column='E', window_size=2)
        self.assertFalse(result['E'].isnull().values.any(), "Smooth time series failed")

    def test_remove_outliers(self):
        result = remove_outliers(self.df, columns=['E'])
        self.assertEqual(len(result), 4, "Remove outliers failed")

    def test_normalize_data(self):
        result = normalize_data(self.df, columns=['E'])
        self.assertTrue(result['E'].between(0, 1).all(), "Normalize data failed")

    def test_encode_categorical(self):
        result = encode_categorical(self.df, columns=['C'])
        self.assertIn('C_b', result.columns, "Encode categorical failed")

    def test_scale_features(self):
        result = scale_features(self.df, columns=['E'])
        self.assertAlmostEqual(result['E'].mean(), 0.0, places=7, msg="Scale features failed")

    def test_handle_imbalanced_data(self):
        X = self.df[['A', 'B', 'E']]
        y = pd.Series([1, 0, 0, 0])
        X_res, y_res = handle_imbalanced_data(X, y)
        self.assertGreater(len(X_res), len(X), "Handle imbalanced data failed")

    def test_log_transform(self):
        result = log_transform(self.df, columns=['E'])
        self.assertTrue((result['E'] > 0).all(), "Log transform failed")

    def test_create_cluster_features(self):
        result = create_cluster_features(self.df, columns=['A', 'B'], n_clusters=2)
        self.assertIn('cluster', result.columns, "Create cluster features failed")

    def test_automated_feature_engineering(self):
        result = automated_feature_engineering(self.df, target_column='E')
        self.assertGreater(len(result.columns), len(self.df.columns), "Automated feature engineering failed")

if __name__ == '__main__':
    unittest.main()
