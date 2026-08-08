"""
EDA + Storytelling — Employee Attrition Analysis
=================================================
Dataset: IBM HR Analytics Employee Attrition & Performance
Download: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
Steps:
    1. Download WA_Fn-UseC_-HR-Employee-Attrition.csv into data/
    2. pip install pandas plotly scipy
    3. python eda_attrition.py
Goal: this is NOT just charts — the deliverable is a short written
narrative (see NARRATIVE.md) backed by 4-5 charts. Interviewers will
ask "so what did you conclude and what would you recommend?" — make
sure you can answer that in one sentence per finding.
"""

import pandas as pd
import plotly.express as px
from scipy import stats

DATA_PATH = "data/WA_Fn-UseC_-HR-Employee-Attrition.csv"


def load_data():
    return pd.read_csv(DATA_PATH)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop constant/useless columns present in this dataset
    drop_cols = ["EmployeeCount", "StandardHours", "Over18", "EmployeeNumber"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    df["Attrition_Flag"] = (df["Attrition"] == "Yes").astype(int)
    return df


def attrition_by_department(df):
    summary = (df.groupby("Department")["Attrition_Flag"]
                 .mean().mul(100).round(1).reset_index()
                 .rename(columns={"Attrition_Flag": "Attrition_Rate_%"}))
    fig = px.bar(summary, x="Department", y="Attrition_Rate_%",
                 title="Attrition Rate by Department", text="Attrition_Rate_%")
    fig.write_html("chart_attrition_by_department.html")
    return summary


def attrition_by_overtime(df):
    summary = (df.groupby("OverTime")["Attrition_Flag"]
                 .mean().mul(100).round(1).reset_index()
                 .rename(columns={"Attrition_Flag": "Attrition_Rate_%"}))
    fig = px.bar(summary, x="OverTime", y="Attrition_Rate_%",
                 title="Attrition Rate: Overtime vs No Overtime", text="Attrition_Rate_%")
    fig.write_html("chart_attrition_by_overtime.html")

    # Statistical significance check (chi-square test)
    contingency = pd.crosstab(df["OverTime"], df["Attrition"])
    chi2, p_value, _, _ = stats.chi2_contingency(contingency)
    print(f"OverTime vs Attrition — chi-square p-value: {p_value:.5f}")
    return summary, p_value


def income_vs_attrition(df):
    fig = px.box(df, x="Attrition", y="MonthlyIncome",
                 title="Monthly Income Distribution: Attrition vs Retained")
    fig.write_html("chart_income_vs_attrition.html")

    left = df[df["Attrition"] == "Yes"]["MonthlyIncome"]
    stayed = df[df["Attrition"] == "No"]["MonthlyIncome"]
    t_stat, p_value = stats.ttest_ind(left, stayed, equal_var=False)
    print(f"Income (left vs stayed) — t-test p-value: {p_value:.5f}")
    return p_value


def tenure_vs_attrition(df):
    fig = px.histogram(df, x="YearsAtCompany", color="Attrition", barmode="overlay",
                        title="Years at Company vs Attrition")
    fig.write_html("chart_tenure_vs_attrition.html")


def job_satisfaction_vs_attrition(df):
    summary = (df.groupby("JobSatisfaction")["Attrition_Flag"]
                 .mean().mul(100).round(1).reset_index()
                 .rename(columns={"Attrition_Flag": "Attrition_Rate_%"}))
    fig = px.line(summary, x="JobSatisfaction", y="Attrition_Rate_%", markers=True,
                  title="Attrition Rate by Job Satisfaction Level (1=Low, 4=High)")
    fig.write_html("chart_satisfaction_vs_attrition.html")
    return summary


if __name__ == "__main__":
    df = clean_data(load_data())
    print("\n--- Attrition by Department ---")
    print(attrition_by_department(df))
    print("\n--- Attrition by Overtime ---")
    summary, p = attrition_by_overtime(df)
    print(summary)
    print("\n--- Income vs Attrition ---")
    income_vs_attrition(df)
    tenure_vs_attrition(df)
    print("\n--- Job Satisfaction vs Attrition ---")
    print(job_satisfaction_vs_attrition(df))
    print("\nAll charts saved as HTML files in this folder.")
