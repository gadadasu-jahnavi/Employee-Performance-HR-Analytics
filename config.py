"""
Configuration file for Employee Performance & HR Analytics Project
"""

import os
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample_templates"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"
VISUALIZATIONS_DIR = REPORTS_DIR / "visualizations"
SUMMARIES_DIR = REPORTS_DIR / "summaries"

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLE_DATA_DIR, 
                   VISUALIZATIONS_DIR, SUMMARIES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File Paths
RAW_DATA_PATH = RAW_DATA_DIR / "employee_data_raw.csv"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "employee_data_processed.csv"
SAMPLE_TEMPLATE_PATH = SAMPLE_DATA_DIR / "data_template.csv"

# Data Processing Configuration
DATA_CONFIG = {
    'missing_value_threshold': 0.5,  # Drop columns with >50% missing values
    'outlier_method': 'iqr',  # 'iqr' or 'zscore'
    'outlier_threshold': 1.5,  # IQR multiplier
    'zscore_threshold': 3,  # Standard deviations
    'test_size': 0.2,
    'random_state': 42
}

# Performance Metrics Configuration
PERFORMANCE_CONFIG = {
    'performance_rating_scale': 5,  # 1-5 scale
    'min_performance': 1,
    'max_performance': 5,
    'high_performer_threshold': 4,  # Rating >= 4
    'low_performer_threshold': 2,  # Rating <= 2
}

# Turnover Analysis Configuration
TURNOVER_CONFIG = {
    'turnover_risk_high': 0.7,  # Probability >= 0.7
    'turnover_risk_medium': 0.4,  # Probability 0.4-0.7
    'turnover_risk_low': 0.0,  # Probability < 0.4
}

# Salary Configuration
SALARY_CONFIG = {
    'min_salary': 30000,
    'max_salary': 500000,
    'currency': 'USD',
    'salary_adjustment_factor': 1.05  # 5% annual increase
}

# Experience Configuration
EXPERIENCE_CONFIG = {
    'junior_threshold': 2,  # Years
    'mid_level_threshold': 5,  # Years
    'senior_threshold': 10,  # Years
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'page_title': 'HR Analytics Dashboard',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'theme': 'light',  # 'light' or 'dark'
    'refresh_interval': 3600,  # Seconds
}

# Model Configuration
MODEL_CONFIG = {
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': 42
    },
    'gradient_boosting': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 5,
        'random_state': 42
    },
    'linear_regression': {
        'fit_intercept': True,
        'normalize': False
    }
}

# Visualization Configuration
VIZ_CONFIG = {
    'figure_size': (12, 6),
    'dpi': 300,
    'style': 'seaborn-v0_8-darkgrid',
    'color_palette': 'husl',
    'font_size': 12,
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': PROJECT_ROOT / 'logs' / 'hr_analytics.log'
}

# Create logs directory
LOGGING_CONFIG['log_file'].parent.mkdir(parents=True, exist_ok=True)

# Columns Definition
COLUMN_DEFINITIONS = {
    'employee_id': 'Unique identifier for each employee',
    'name': 'Employee full name',
    'department': 'Department assignment',
    'job_title': 'Current job title/position',
    'performance_rating': 'Performance rating (1-5 scale)',
    'salary': 'Annual salary in USD',
    'experience_years': 'Years of experience with company',
    'age': 'Employee age in years',
    'joining_date': 'Date of joining the company',
    'promotion_eligible': 'Whether eligible for promotion (Yes/No)',
    'attrition_risk': 'Risk of employee attrition (High/Medium/Low)',
    'education': 'Educational qualification',
    'location': 'Work location/office',
    'gender': 'Gender (Male/Female/Other)',
}

# Department List
DEPARTMENTS = [
    'IT',
    'HR',
    'Finance',
    'Operations',
    'Sales',
    'Marketing',
    'Customer Service',
    'Research & Development'
]

# Job Titles
JOB_TITLES = [
    'Junior Developer',
    'Senior Developer',
    'Tech Lead',
    'HR Manager',
    'Financial Analyst',
    'Operations Manager',
    'Sales Executive',
    'Marketing Manager',
    'Product Manager',
    'Data Scientist',
    'Quality Assurance',
    'Business Analyst'
]

# Analysis Parameters
ANALYSIS_PARAMS = {
    'correlation_threshold': 0.7,  # Correlation coefficient threshold
    'significance_level': 0.05,  # Statistical significance level
    'confidence_level': 0.95,  # Confidence interval level
}

if __name__ == '__main__':
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Reports Directory: {REPORTS_DIR}")
    print("Configuration loaded successfully!")