# Employee Performance & HR Analytics

A comprehensive data analytics project using Python to analyze employee performance, HR metrics, and organizational workforce insights.

## 📊 Project Overview

This project provides an end-to-end solution for:
- Employee performance tracking and evaluation
- HR metrics analysis and reporting
- Workforce analytics and trend identification
- Data visualization and dashboard creation
- Predictive analytics for HR insights

## 🎯 Key Features

✅ **Data Cleaning & Preprocessing** - Handle missing values, outliers, and data quality issues
✅ **Exploratory Data Analysis (EDA)** - Comprehensive statistical analysis
✅ **Performance Metrics** - Calculate KPIs for individual and team performance
✅ **Interactive Dashboard** - Visualize key HR metrics
✅ **Predictive Models** - Employee turnover and performance predictions
✅ **Report Generation** - Automated PDF and Excel reports
✅ **Data Visualization** - Multiple chart types for insights

## 📁 Project Structure

```
Employee-Performance-HR-Analytics/
├── data/
│   ├── raw/
│   │   └── employee_data_raw.csv
│   ├── processed/
│   │   └── employee_data_processed.csv
│   └── sample_templates/
│       └── data_template.csv
├── scripts/
│   ├── data_cleaning.py
│   ├── eda_analysis.py
│   ├── performance_metrics.py
│   ├── predictive_models.py
│   └── utils.py
├── dashboard/
│   ├── dashboard.py
│   ├── app.py
│   └── requirements.txt
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_employee_performance_analysis.ipynb
│   ├── 03_predictive_analytics.ipynb
│   └── 04_dashboard_creation.ipynb
├── reports/
│   ├── visualizations/
│   └── summaries/
├── requirements.txt
├── config.py
├── README.md
└── LICENSE
```

## 🛠️ Tech Stack

- **Python 3.8+**
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **Matplotlib & Seaborn** - Static visualizations
- **Plotly** - Interactive visualizations
- **Streamlit** - Dashboard framework
- **Jupyter** - Exploratory analysis

## 📊 Analytics Performed

### 1. Employee Performance Analysis
- Performance ratings distribution
- Department-wise performance comparison
- Performance vs compensation analysis
- Promotion eligibility assessment

### 2. HR Metrics
- Employee turnover rate
- Retention analysis
- Recruitment funnel
- Salary equity analysis
- Experience distribution

### 3. Predictive Analytics
- Employee turnover prediction
- Performance prediction
- Salary recommendations
- Career progression paths

## 🚀 Quick Start

### Prerequisites
```bash
python >= 3.8
pip
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/gadadasu-jahnavi/Employee-Performance-HR-Analytics.git
cd Employee-Performance-HR-Analytics
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Usage

#### 1. Data Cleaning & Preprocessing
```bash
python scripts/data_cleaning.py
```

#### 2. Exploratory Data Analysis
```bash
python scripts/eda_analysis.py
```

#### 3. Calculate Performance Metrics
```bash
python scripts/performance_metrics.py
```

#### 4. Run Predictive Models
```bash
python scripts/predictive_models.py
```

#### 5. Launch Interactive Dashboard
```bash
streamlit run dashboard/app.py
```

#### 6. Run Jupyter Notebooks
```bash
jupyter notebook
```

## 📈 Dashboard Features

The Streamlit dashboard includes:

1. **Overview Metrics**
   - Total employees
   - Average performance rating
   - Turnover rate
   - Department count

2. **Performance Analysis**
   - Performance distribution by department
   - Performance vs compensation scatter plot
   - Top performers list
   - Performance trends over time

3. **HR Metrics**
   - Employee retention analysis
   - Salary distribution
   - Experience distribution
   - Department headcount

4. **Predictive Insights**
   - Turnover risk employees
   - Performance predictions
   - Salary recommendations
   - Career progression suggestions

## 📊 Sample Data Description

The sample dataset includes:
- **Employee ID**: Unique identifier
- **Name**: Employee name
- **Department**: Department assignment
- **Job Title**: Current job title
- **Performance Rating**: 1-5 scale
- **Salary**: Annual salary
- **Experience (Years)**: Years with company
- **Age**: Employee age
- **Joining Date**: Employment start date
- **Promotion Eligible**: Yes/No
- **Attrition Risk**: High/Medium/Low

## 🔧 Configuration

Edit `config.py` to customize:
- File paths
- Analysis parameters
- Model hyperparameters
- Dashboard settings

## 📈 Analysis Outputs

### Generated Reports
- `reports/visualizations/` - PNG/PDF charts
- `reports/summaries/` - Statistical summaries
- `data/processed/` - Cleaned datasets

### Visualizations
- Performance distribution histograms
- Department comparison bar charts
- Correlation heatmaps
- Trend line plots
- Box plots for outlier detection
- Scatter plots for relationships

## 🤖 Predictive Models Included

1. **Turnover Prediction Model**
   - Algorithm: Random Forest Classifier
   - Features: Experience, salary, performance, age, department
   - Output: Turnover risk score (0-1)

2. **Performance Prediction Model**
   - Algorithm: Gradient Boosting Regressor
   - Features: Historical performance, department, experience
   - Output: Expected performance rating

3. **Salary Recommendation Model**
   - Algorithm: Linear Regression
   - Features: Experience, performance, department, job title
   - Output: Recommended salary range

## 📝 Data Privacy & Security

- All employee data is handled with care
- Sensitive information is anonymized in reports
- Follow GDPR and data protection guidelines
- Secure file handling and encryption recommended

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Authors

- **Jahnavi Gadadasu** - Project Developer

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: gadadasu.jahnavi@example.com

## 🙏 Acknowledgments

- Data analytics best practices
- Python data science community
- Open-source libraries contributors

## 📚 References

- [Pandas Documentation](https://pandas.pydata.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [HR Analytics Best Practices](https://www.hr.com/)

---

**Last Updated**: October 2026
**Version**: 1.0.0