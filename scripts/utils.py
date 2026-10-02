"""
Utility functions for HR Analytics Project
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Tuple, List, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from CSV file with error handling
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}")
        logger.info(f"Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def save_data(df: pd.DataFrame, file_path: str, index: bool = False) -> None:
    """
    Save DataFrame to CSV file
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=index)
        logger.info(f"Data saved successfully to {file_path}")
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise

def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check and report missing values
    """
    missing_data = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum().values,
        'Missing_Percentage': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    missing_data = missing_data[missing_data['Missing_Count'] > 0].sort_values('Missing_Percentage', ascending=False)
    
    if not missing_data.empty:
        logger.info("Missing Values Report:")
        logger.info(missing_data.to_string())
    else:
        logger.info("No missing values found")
    
    return missing_data

def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
    """
    Remove duplicate rows
    """
    initial_rows = len(df)
    df = df.drop_duplicates(subset=subset)
    removed_rows = initial_rows - len(df)
    
    if removed_rows > 0:
        logger.info(f"Removed {removed_rows} duplicate rows")
    else:
        logger.info("No duplicate rows found")
    
    return df

def handle_outliers(df: pd.DataFrame, columns: List[str], method: str = 'iqr', threshold: float = 1.5) -> Tuple[pd.DataFrame, Dict]:
    """
    Handle outliers using IQR or Z-score method
    """
    outlier_info = {}
    
    for col in columns:
        if col not in df.columns:
            logger.warning(f"Column {col} not found in DataFrame")
            continue
        
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_info[col] = {
                'method': 'IQR',
                'outlier_count': len(outliers),
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
            
            # Cap outliers instead of removing them
            df[col] = df[col].clip(lower_bound, upper_bound)
        
        elif method == 'zscore':
            from scipy import stats
            z_scores = np.abs(stats.zscore(df[col]))
            outliers = df[z_scores > threshold]
            outlier_info[col] = {
                'method': 'Z-score',
                'outlier_count': len(outliers),
                'threshold': threshold
            }
            
            df = df[z_scores <= threshold]
    
    logger.info(f"Outlier handling completed using {method} method")
    return df, outlier_info

def encode_categorical(df: pd.DataFrame, columns: List[str] = None) -> Tuple[pd.DataFrame, Dict]:
    """
    Encode categorical variables
    """
    encoders = {}
    
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns.tolist()
    
    for col in columns:
        if col in df.columns and df[col].dtype == 'object':
            le = LabelEncoder()
            df[f'{col}_encoded'] = le.fit_transform(df[col])
            encoders[col] = le
            logger.info(f"Encoded column: {col}")
    
    return df, encoders

def scale_numerical(df: pd.DataFrame, columns: List[str] = None) -> Tuple[pd.DataFrame, StandardScaler]:
    """
    Scale numerical features
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    logger.info(f"Scaled {len(columns)} numerical columns")
    
    return df, scaler

def generate_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary statistics
    """
    summary = df.describe().T
    logger.info("Summary statistics generated")
    return summary

def create_correlation_matrix(df: pd.DataFrame, numeric_only: bool = True) -> pd.DataFrame:
    """
    Create correlation matrix for numerical features
    """
    if numeric_only:
        df_numeric = df.select_dtypes(include=[np.number])
    else:
        df_numeric = df
    
    corr_matrix = df_numeric.corr()
    logger.info("Correlation matrix created")
    return corr_matrix

def plot_correlation_heatmap(corr_matrix: pd.DataFrame, figsize: Tuple[int, int] = (12, 10), save_path: str = None) -> None:
    """
    Plot correlation matrix as heatmap
    """
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix Heatmap', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=config.VIZ_CONFIG['dpi'])
        logger.info(f"Heatmap saved to {save_path}")
    
    plt.close()

def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get comprehensive information about the dataset
    """
    info = {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
        'dtypes': df.dtypes.value_counts().to_dict(),
        'missing_values': df.isnull().sum().sum(),
        'duplicates': df.duplicated().sum(),
        'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
        'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
    }
    return info

def print_data_info(df: pd.DataFrame) -> None:
    """
    Print comprehensive data information
    """
    info = get_data_info(df)
    logger.info("\n" + "="*50)
    logger.info("DATA INFORMATION")
    logger.info("="*50)
    logger.info(f"Rows: {info['rows']}")
    logger.info(f"Columns: {info['columns']}")
    logger.info(f"Memory Usage: {info['memory_usage']:.2f} MB")
    logger.info(f"Missing Values: {info['missing_values']}")
    logger.info(f"Duplicates: {info['duplicates']}")
    logger.info(f"Numeric Columns: {len(info['numeric_columns'])}")
    logger.info(f"Categorical Columns: {len(info['categorical_columns'])}")
    logger.info("="*50 + "\n")

if __name__ == '__main__':
    print("Utility functions module loaded successfully")