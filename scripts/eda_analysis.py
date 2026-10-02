"""
Exploratory Data Analysis (EDA) for Employee Data
Generate statistical summaries, distributions, and relationships
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from typing import Dict, List
import config
from utils import (
    load_data, save_data, generate_summary_stats,
    create_correlation_matrix, plot_correlation_heatmap
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class EmployeeEDA:
    """
    Exploratory Data Analysis class for employee data
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        logger.info(f"Initialized EDA with {len(df)} rows and {len(df.columns)} columns")
    
    def basic_statistics(self) -> pd.DataFrame:
        """
        Generate basic statistical summary
        """
        logger.info("Generating basic statistics...")
        stats = generate_summary_stats(self.df[self.numeric_cols])
        logger.info("Basic statistics generated")
        return stats
    
    def correlation_analysis(self) -> pd.DataFrame:
        """
        Analyze correlations between numerical variables
        """
        logger.info("Performing correlation analysis...")
        corr_matrix = create_correlation_matrix(self.df, numeric_only=True)
        
        # Find strong correlations (>0.7)
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > config.ANALYSIS_PARAMS['correlation_threshold']:
                    strong_corr.append({
                        'Variable 1': corr_matrix.columns[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
        
        if strong_corr:
            strong_corr_df = pd.DataFrame(strong_corr)
            logger.info(f"Found {len(strong_corr)} strong correlations (>0.7)")
            logger.info(strong_corr_df.to_string())
        
        return corr_matrix
    
    def distribution_analysis(self) -> None:
        """
        Analyze distributions of numerical variables
        """
        logger.info("Performing distribution analysis...")
        
        for col in self.numeric_cols:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            # Histogram
            axes[0].hist(self.df[col], bins=30, edgecolor='black', alpha=0.7)
            axes[0].set_xlabel(col)
            axes[0].set_ylabel('Frequency')
            axes[0].set_title(f'Distribution of {col}')
            axes[0].grid(True, alpha=0.3)
            
            # Box plot
            axes[1].boxplot(self.df[col])
            axes[1].set_ylabel(col)
            axes[1].set_title(f'Box Plot of {col}')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            save_path = config.VISUALIZATIONS_DIR / f'{col}_distribution.png'
            plt.savefig(save_path, dpi=config.VIZ_CONFIG['dpi'], bbox_inches='tight')
            logger.info(f"Saved distribution plot: {save_path}")
            plt.close()
    
    def categorical_analysis(self) -> None:
        """
        Analyze categorical variables
        """
        logger.info("Performing categorical analysis...")
        
        for col in self.categorical_cols:
            if col not in ['employee_id', 'name', 'joining_date']:  # Skip ID and date columns
                fig, ax = plt.subplots(figsize=(12, 6))
                
                value_counts = self.df[col].value_counts()
                colors = sns.color_palette("husl", len(value_counts))
                
                value_counts.plot(kind='bar', ax=ax, color=colors)
                ax.set_title(f'Distribution of {col}', fontsize=14, fontweight='bold')
                ax.set_xlabel(col)
                ax.set_ylabel('Count')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                save_path = config.VISUALIZATIONS_DIR / f'{col}_distribution.png'
                plt.savefig(save_path, dpi=config.VIZ_CONFIG['dpi'], bbox_inches='tight')
                logger.info(f"Saved categorical plot: {save_path}")
                plt.close()
    
    def department_analysis(self) -> pd.DataFrame:
        """
        Analyze metrics by department
        """
        logger.info("Performing department analysis...")
        
        if 'department' not in self.df.columns:
            logger.warning("Department column not found")
            return pd.DataFrame()
        
        dept_analysis = self.df.groupby('department').agg({
            'employee_id': 'count',
            'salary': ['mean', 'median', 'std'],
            'performance_rating': ['mean', 'count'] if 'performance_rating' in self.df.columns else {},
            'experience_years': 'mean' if 'experience_years' in self.df.columns else {},
            'age': 'mean' if 'age' in self.df.columns else {}
        }).round(2)
        
        logger.info("Department Analysis:")
        logger.info(dept_analysis.to_string())
        
        # Visualize department stats
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        if 'performance_rating' in self.df.columns:
            self.df.groupby('department')['performance_rating'].mean().plot(kind='bar', ax=axes[0, 0], color='skyblue')
            axes[0, 0].set_title('Average Performance Rating by Department')
            axes[0, 0].set_ylabel('Rating')
        
        self.df.groupby('department')['salary'].mean().plot(kind='bar', ax=axes[0, 1], color='lightgreen')
        axes[0, 1].set_title('Average Salary by Department')
        axes[0, 1].set_ylabel('Salary')
        
        if 'experience_years' in self.df.columns:
            self.df.groupby('department')['experience_years'].mean().plot(kind='bar', ax=axes[1, 0], color='lightcoral')
            axes[1, 0].set_title('Average Experience by Department')
            axes[1, 0].set_ylabel('Years')
        
        self.df['department'].value_counts().plot(kind='bar', ax=axes[1, 1], color='plum')
        axes[1, 1].set_title('Employee Count by Department')
        axes[1, 1].set_ylabel('Count')
        
        plt.tight_layout()
        save_path = config.VISUALIZATIONS_DIR / 'department_analysis.png'
        plt.savefig(save_path, dpi=config.VIZ_CONFIG['dpi'], bbox_inches='tight')
        logger.info(f"Saved department analysis plot: {save_path}")
        plt.close()
        
        return dept_analysis
    
    def salary_analysis(self) -> Dict:
        """
        Comprehensive salary analysis
        """
        logger.info("Performing salary analysis...")
        
        if 'salary' not in self.df.columns:
            logger.warning("Salary column not found")
            return {}
        
        salary_stats = {
            'mean': self.df['salary'].mean(),
            'median': self.df['salary'].median(),
            'std': self.df['salary'].std(),
            'min': self.df['salary'].min(),
            'max': self.df['salary'].max(),
            'q1': self.df['salary'].quantile(0.25),
            'q3': self.df['salary'].quantile(0.75)
        }
        
        logger.info("Salary Statistics:")
        for key, value in salary_stats.items():
            logger.info(f"  {key.upper()}: ${value:,.2f}")
        
        return salary_stats
    
    def performance_analysis(self) -> Dict:
        """
        Comprehensive performance analysis
        """
        logger.info("Performing performance analysis...")
        
        if 'performance_rating' not in self.df.columns:
            logger.warning("Performance rating column not found")
            return {}
        
        performance_dist = self.df['performance_rating'].value_counts().sort_index()
        
        perf_stats = {
            'mean': self.df['performance_rating'].mean(),
            'median': self.df['performance_rating'].median(),
            'std': self.df['performance_rating'].std(),
            'distribution': performance_dist.to_dict()
        }
        
        logger.info("Performance Rating Distribution:")
        logger.info(self.df['performance_rating'].value_counts().sort_index().to_string())
        
        return perf_stats
    
    def generate_eda_report(self) -> None:
        """
        Generate comprehensive EDA report
        """
        logger.info("\n" + "="*60)
        logger.info("GENERATING COMPREHENSIVE EDA REPORT")
        logger.info("="*60 + "\n")
        
        # Basic statistics
        logger.info("[1] BASIC STATISTICS")
        stats = self.basic_statistics()
        stats_path = config.SUMMARIES_DIR / 'basic_statistics.csv'
        stats.to_csv(stats_path)
        logger.info(f"Saved to: {stats_path}\n")
        
        # Correlation analysis
        logger.info("[2] CORRELATION ANALYSIS")
        corr_matrix = self.correlation_analysis()
        corr_path = config.SUMMARIES_DIR / 'correlation_matrix.csv'
        corr_matrix.to_csv(corr_path)
        plot_correlation_heatmap(corr_matrix, save_path=config.VISUALIZATIONS_DIR / 'correlation_heatmap.png')
        logger.info(f"Saved to: {corr_path}\n")
        
        # Distribution analysis
        logger.info("[3] DISTRIBUTION ANALYSIS")
        self.distribution_analysis()
        logger.info()
        
        # Categorical analysis
        logger.info("[4] CATEGORICAL ANALYSIS")
        self.categorical_analysis()
        logger.info()
        
        # Department analysis
        logger.info("[5] DEPARTMENT ANALYSIS")
        dept_stats = self.department_analysis()
        logger.info()
        
        # Salary analysis
        logger.info("[6] SALARY ANALYSIS")
        salary_stats = self.salary_analysis()
        logger.info()
        
        # Performance analysis
        logger.info("[7] PERFORMANCE ANALYSIS")
        perf_stats = self.performance_analysis()
        logger.info()
        
        logger.info("="*60)
        logger.info("EDA REPORT GENERATION COMPLETED")
        logger.info("="*60)

def main():
    """
    Main execution function
    """
    try:
        logger.info("Loading processed employee data...")
        df = load_data(str(config.PROCESSED_DATA_PATH))
        
        logger.info("Initializing EDA analysis...")
        eda = EmployeeEDA(df)
        
        logger.info("Generating EDA report...")
        eda.generate_eda_report()
        
        logger.info(f"\nAll visualizations saved to: {config.VISUALIZATIONS_DIR}")
        logger.info(f"All summaries saved to: {config.SUMMARIES_DIR}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == '__main__':
    main()