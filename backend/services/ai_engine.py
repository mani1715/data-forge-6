import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer

class AIEngine:
    
    @staticmethod
    def clean_missing_values(df, strategy='ai', fill_value=None):
        """
        Handles missing values for Numeric columns.
        Strategies: 'ai', 'mean', 'median', 'mode', 'constant', 'drop'
        """
        df_clean = df.copy()
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        
        message = ""

        if strategy == 'drop_rows':
            initial_rows = len(df_clean)
            df_clean = df_clean.dropna()
            message = f"Dropped {initial_rows - len(df_clean)} rows containing missing values."
            return df_clean, message

        if len(numeric_cols) > 0:
            if strategy == 'ai':
                imputer = IterativeImputer(random_state=42)
                df_clean[numeric_cols] = imputer.fit_transform(df_clean[numeric_cols])
                message = "Applied AI-based Imputation (MICE Algorithm)."
                
            elif strategy == 'mean':
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
                message = "Filled missing values with Column Means."
                
            elif strategy == 'median':
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
                message = "Filled missing values with Column Medians."
            
            elif strategy == 'mode':
                for col in numeric_cols:
                    mode_val = df_clean[col].mode()
                    if not mode_val.empty:
                        df_clean[col] = df_clean[col].fillna(mode_val[0])
                message = "Filled missing values with Mode."

            elif strategy == 'constant':
                val = fill_value if fill_value is not None else 0
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(val)
                message = f"Filled missing values with constant value: {val}."
        else:
            message = "No numeric columns found to clean."
        
        return df_clean, message

    @staticmethod
    def remove_outliers(df):
        """
        Removes outliers using the IQR method for Numeric columns.
        """
        df_clean = df.copy()
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        initial_rows = len(df_clean)
        
        for col in numeric_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
            
        rows_removed = initial_rows - len(df_clean)
        return df_clean, f"Removed {rows_removed} outliers using IQR method."

    @staticmethod
    def clean_categorical_data(df, strategy='unknown'):
        """
        Handles missing values for Text/Categorical columns.
        Strategy: 'unknown' fills with 'Unknown', 'mode' fills with most frequent.
        """
        df_clean = df.copy()
        cat_cols = df_clean.select_dtypes(include=['object']).columns
        
        if len(cat_cols) == 0:
            return df_clean, "No text columns found to clean."

        filled_count = 0
        
        for col in cat_cols:
            if df_clean[col].isnull().sum() > 0:
                if strategy == 'mode':
                    mode_val = df_clean[col].mode()
                    if not mode_val.empty:
                        df_clean[col] = df_clean[col].fillna(mode_val[0])
                        filled_count += 1
                else:
                    # Default: Fill with 'Unknown'
                    df_clean[col] = df_clean[col].fillna('Unknown')
                    filled_count += 1
        
        msg = f"Cleaned {filled_count} text columns using strategy: {strategy}."
        return df_clean, msg