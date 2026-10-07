# Employee Attrition Analytics

🚀 **[Live Dashboard](https://employee-attrition-analytics-j9unz5sn4bgwew6uant6p7.streamlit.app/)**

An interactive HR analytics dashboard built with Python, Streamlit and statistical analysis.

A recruiter-ready HR analytics project focused on **employee attrition, high-risk roles, overtime exposure and statistical evidence**.

## Business question

**Which employee segments are most associated with attrition, and where should HR focus retention efforts?**

## Dataset

IBM HR Analytics Employee Attrition & Performance dataset.

## Stack

- Python
- pandas / NumPy
- Plotly
- SciPy
- Streamlit
- Optional SQL practice

## Dashboard features

### KPI cards
- Employees: **1,470**
- Attrition rate: **16.1%**
- Employees who left: **237**
- Average monthly income: **$6,503**

### Interactive filters
- Department
- Job role
- Overtime

### Visual analysis
- Attrition rate by department
- Attrition rate by job role
- Overtime vs attrition
- Attrition by tenure
- Monthly income distribution by attrition status
- Job satisfaction vs attrition

### Statistical evidence
- Chi-square test for **Overtime × Attrition**
- Welch's t-test for **Monthly Income × Attrition**

## Key findings from the full dataset

- Overall attrition rate: **16.1%**
- Overtime: **30.5%** attrition
- No overtime: **10.4%** attrition
- Highest-risk job role: **Sales Representative (39.8%)**
- Average monthly income — employees who left: **$4,787**
- Average monthly income — employees who stayed: **$6,833**
- Overtime chi-square p-value: **8.16e-21**
- Monthly income Welch t-test p-value: **4.43e-13**

## Interpretation

Employees who work overtime have a substantially higher attrition rate than employees who do not. The overtime/attrition association is statistically significant in this dataset.

Monthly income also differs significantly between employees who left and stayed.

The analysis identifies **Sales Representatives** as a particularly high-risk job role in the full dataset, making role-specific retention interventions worth investigating.

### Important statistical caveat

This dataset is observational. A statistically significant association **does not prove causation**. For example, the overtime result does not by itself prove that overtime causes employees to leave. A real HR decision should be validated using longitudinal data, employee surveys and operational context.

## Recommended business actions

1. **Monitor sustained overtime** and investigate teams with consistently high overtime exposure.
2. **Prioritize high-risk job roles** for retention interviews and manager review.
3. **Strengthen first-year retention**, including onboarding, mentoring and career-path conversations.
4. **Review compensation and workload together**, rather than assuming salary alone explains attrition.
5. Track these KPIs over time to measure whether interventions actually reduce attrition.

## How to run

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Portfolio interview explanation

> "I analyzed employee attrition using Python and statistical testing. I built an interactive Streamlit dashboard to identify high-risk roles and workforce patterns, then used a chi-square test and Welch's t-test to quantify evidence for relationships involving overtime and income. I treated the results as associations rather than causal claims and translated the findings into practical retention recommendations."

## Files

- `dashboard.py` — interactive Streamlit dashboard
- `queries.sql` — optional SQL versions of key analyses
- `requirements.txt` — dependencies
- `data/` — dataset used by the project
- `NARRATIVE.md` — original narrative retained for reference
