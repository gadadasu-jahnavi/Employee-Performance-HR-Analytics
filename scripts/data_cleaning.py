"""
Data Cleaning and Preprocessing Script
Handles missing values, duplicates, outliers, and data quality issues
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple
import config
from utils import (
    load_data, save_data, check_missing_values, remove_duplicates,
    handle_outliers, encode_categorical, print_data_info
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def clean_employee_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Comprehensive data cleaning pipeline
    """
    logger.info("Starting data cleaning pipeline...")
    print_data_info(df)
    
    # Step 1: Check and report missing values
    logger.info("\n[STEP 1] Checking missing values...")
    missing_df = check_missing_values(df)
    
    # Step 2: Handle missing values
    logger.info("\n[STEP 2] Handling missing values...")
    df = df.dropna(subset=['employee_id', 'name', 'department'])  # Drop rows with critical missing values
    
    # Fill numerical missing values with mean
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mean(), inplace=True)
            logger.info(f"Filled missing values in {col} with mean")
    
    # Fill categorical missing values with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
            logger.info(f"Filled missing values in {col} with mode")
    
    # Step 3: Remove duplicates
    logger.info("\n[STEP 3] Removing duplicates...")
    df = remove_duplicates(df, subset=['employee_id', 'name'])
    
    # Step 4: Data type validation and conversion
    logger.info("\n[STEP 4] Validating and converting data types...")
    if 'joining_date' in df.columns:
        df['joining_date'] = pd.to_datetime(df['joining_date'], errors='coerce')
    
    if 'salary' in df.columns:
        df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
    
    if 'performance_rating' in df.columns:
        df['performance_rating'] = pd.to_numeric(df['performance_rating'], errors='coerce')
    
    if 'experience_years' in df.columns:
        df['experience_years'] = pd.to_numeric(df['experience_years'], errors='coerce')
    
    # Step 5: Handle outliers
    logger.info("\n[STEP 5] Handling outliers...")
    numerical_cols_to_check = ['salary', 'performance_rating', 'experience_years', 'age']
    numerical_cols_to_check = [col for col in numerical_cols_to_check if col in df.columns]
    
    df, outlier_info = handle_outliers(
        df,
        columns=numerical_cols_to_check,
        method=config.DATA_CONFIG['outlier_method'],
        threshold=config.DATA_CONFIG['outlier_threshold']
    )
    
    for col, info in outlier_info.items():
        logger.info(f"  {col}: {info['outlier_count']} outliers handled")
    
    # Step 6: Validate ranges
    logger.info("\n[STEP 6] Validating value ranges...")
    if 'performance_rating' in df.columns:
        df['performance_rating'] = df['performance_rating'].clip(
            config.PERFORMANCE_CONFIG['min_performance'],
            config.PERFORMANCE_CONFIG['max_performance']
        )
    
    if 'salary' in df.columns:
        df['salary'] = df['salary'].clip(
            config.SALARY_CONFIG['min_salary'],
            config.SALARY_CONFIG['max_salary']
        )
    
    if 'age' in df.columns:
        df = df[df['age'] >= 18]  # Remove invalid ages
    
    # Step 7: Feature engineering
    logger.info("\n[STEP 7] Feature engineering...")
    
    if 'experience_years' in df.columns:
        # Create experience level category
        df['experience_level'] = pd.cut(
            df['experience_years'],
            bins=[0, config.EXPERIENCE_CONFIG['junior_threshold'],
                  config.EXPERIENCE_CONFIG['mid_level_threshold'],
                  config.EXPERIENCE_CONFIG['senior_threshold'], float('inf')],
            labels=['Junior', 'Mid-Level', 'Senior', 'Expert']
        )
        logger.info("Created experience_level category")
    
    if 'salary' in df.columns and 'experience_years' in df.columns:
        # Calculate salary per year of experience
        df['salary_per_experience'] = df['salary'] / (df['experience_years'] + 1)
        logger.info("Created salary_per_experience feature")
    
    if 'performance_rating' in df.columns:
        # Create performance category
        df['performance_category'] = pd.cut(
            df['performance_rating'],
            bins=[0, 2, 3, 4, 5],
            labels=['Low', 'Average', 'Good', 'Excellent'],
            include_lowest=True
        )
        logger.info("Created performance_category")
    
    # Step 8: Remove rows with still-invalid data
    logger.info("\n[STEP 8] Final data validation...")
    initial_rows = len(df)
    df = df.dropna()
    removed_rows = initial_rows - len(df)
    if removed_rows > 0:
        logger.info(f"Removed {removed_rows} rows with invalid data after processing")
    
    # Step 9: Reset index
    df.reset_index(drop=True, inplace=True)
    
    logger.info("\n" + "="*50)
    logger.info("Data cleaning completed successfully!")
    logger.info("="*50)
    print_data_info(df)
    
    return df

def validate_cleaned_data(df: pd.DataFrame) -> bool:
    """
    Validate the cleaned dataset
    """
    logger.info("\nValidating cleaned data...")
    
    checks = {
        'No missing values': df.isnull().sum().sum() == 0,
        'No duplicates': df.duplicated().sum() == 0,
        'Minimum rows': len(df) > 0,
        'Valid performance ratings': (df['performance_rating'] >= 1).all() and (df['performance_rating'] <= 5).all() if 'performance_rating' in df.columns else True,
        'Valid salaries': (df['salary'] > 0).all() if 'salary' in df.columns else True,
    }
    
    all_passed = True
    for check, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"  {status}: {check}")
        if not result:
            all_passed = False
    
    return all_passed

def main():
    """
    Main execution function
    """
    try:
        logger.info("Loading raw employee data...")
        df = load_data(str(config.RAW_DATA_PATH))
        
        logger.info("Applying data cleaning pipeline...")
        df_cleaned = clean_employee_data(df)
        
        logger.info("Validating cleaned data...")
        if validate_cleaned_data(df_cleaned):
            logger.info("All validation checks passed!")
        else:
            logger.warning("Some validation checks failed. Review the data.")
        
        logger.info("Saving processed data...")
        save_data(df_cleaned, str(config.PROCESSED_DATA_PATH))
        
        logger.info("\n" + "="*50)
        logger.info("Data cleaning pipeline completed!")
        logger.info(f"Output: {config.PROCESSED_DATA_PATH}")
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == '__main__':
    main()