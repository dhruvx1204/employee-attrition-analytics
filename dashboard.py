
"""
Employee Attrition Analytics Dashboard
======================================
Recruiter-ready HR analytics project using the IBM HR Analytics dataset.

Run:
    pip install -r requirements.txt
    streamlit run dashboard.py
"""

from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from scipy.stats import chi2_contingency, ttest_ind

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

st.set_page_config(
    page_title="Employee Attrition Analytics",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1450px;}
    .hero h1 {font-size:2.25rem; margin-bottom:.15rem;}
    .hero p {color:#667085; margin-top:0;}
    .section-title {font-size:1.15rem; font-weight:700; margin:1rem 0 .45rem;}
    .insight {padding:.85rem 1rem; border:1px solid #eaecf0; border-radius:12px;
              background:#fff; min-height:90px;}
    .note {padding:.75rem 1rem; border-left:4px solid #98a2b3; background:#f8fafc;
           border-radius:8px; color:#475467;}
    .muted {color:#667085; font-size:.86rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data():
    csvs = list(DATA_DIR.glob("*.csv"))
    if not csvs:
        raise FileNotFoundError("No CSV dataset found in the data folder.")
    for path in csvs:
        sample = pd.read_csv(path, nrows=2)
        if {"Attrition", "JobRole", "MonthlyIncome"}.issubset(sample.columns):
            df = pd.read_csv(path)
            break
    else:
        raise FileNotFoundError("IBM HR attrition dataset not found.")
    df["Attrition_Flag"] = (df["Attrition"].str.strip().str.lower() == "yes").astype(int)
    df["OverTime_Flag"] = (df["OverTime"].str.strip().str.lower() == "yes").astype(int)
    df["Tenure_Band"] = pd.cut(
        df["YearsAtCompany"],
        bins=[-1, 1, 2, 5, 10, 40],
        labels=["0–1", "2", "3–5", "6–10", "11+"],
    )
    return df

def pct(x):
    return f"{x:.1f}%"

def main():
    df = load_data()

    st.markdown(
        """
        <div class="hero">
            <h1>Employee Attrition Analytics</h1>
            <p>Identifying attrition patterns, high-risk roles and statistically significant relationships.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Dashboard filters")
        departments = sorted(df["Department"].dropna().unique())
        roles = sorted(df["JobRole"].dropna().unique())
        overtime = sorted(df["OverTime"].dropna().unique())
        selected_departments = st.multiselect("Department", departments, default=[])
        selected_roles = st.multiselect("Job role", roles, default=[])
        selected_overtime = st.multiselect("Overtime", overtime, default=[])

        st.divider()
        st.caption("Use filters to explore employee segments.")
        st.caption("Statistical tests below use the currently filtered employee population.")

    filtered = df.copy()
    if selected_departments:
        filtered = filtered[filtered["Department"].isin(selected_departments)]
    if selected_roles:
        filtered = filtered[filtered["JobRole"].isin(selected_roles)]
    if selected_overtime:
        filtered = filtered[filtered["OverTime"].isin(selected_overtime)]

    if filtered.empty:
        st.warning("No employees match the selected filters.")
        return

    employees = len(filtered)
    left = int(filtered["Attrition_Flag"].sum())
    attrition = filtered["Attrition_Flag"].mean() * 100
    avg_income = filtered["MonthlyIncome"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Employees", f"{employees:,}")
    c2.metric("Attrition rate", f"{attrition:.1f}%")
    c3.metric("Employees left", f"{left:,}")
    c4.metric("Avg. monthly income", f"${avg_income:,.0f}")

    st.markdown('<div class="section-title">Attrition overview</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    dept = (
        filtered.groupby("Department", as_index=False)["Attrition_Flag"]
        .mean()
        .assign(Attrition_Rate=lambda x: x["Attrition_Flag"] * 100)
        .sort_values("Attrition_Rate")
    )
    role = (
        filtered.groupby("JobRole", as_index=False)
        .agg(Attrition_Rate=("Attrition_Flag", "mean"), Employees=("Attrition_Flag", "size"))
    )
    role["Attrition_Rate"] *= 100
    role = role.sort_values("Attrition_Rate")

    with col1:
        fig = px.bar(
            dept, x="Attrition_Rate", y="Department", orientation="h",
            title="Attrition rate by department",
            labels={"Attrition_Rate": "Attrition rate (%)", "Department": ""},
            text="Attrition_Rate",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(height=360, margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        fig = px.bar(
            role, x="Attrition_Rate", y="JobRole", orientation="h",
            title="Attrition rate by job role",
            labels={"Attrition_Rate": "Attrition rate (%)", "JobRole": ""},
            text="Attrition_Rate",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(height=360, margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    col3, col4 = st.columns(2)

    overtime = (
        filtered.groupby("OverTime", as_index=False)["Attrition_Flag"]
        .mean()
        .assign(Attrition_Rate=lambda x: x["Attrition_Flag"] * 100)
    )
    tenure = (
        filtered.groupby("Tenure_Band", observed=False, as_index=False)["Attrition_Flag"]
        .mean()
        .assign(Attrition_Rate=lambda x: x["Attrition_Flag"] * 100)
    )

    with col3:
        fig = px.bar(
            overtime, x="OverTime", y="Attrition_Rate",
            title="Overtime is strongly associated with attrition",
            labels={"Attrition_Rate": "Attrition rate (%)", "OverTime": "Overtime"},
            text="Attrition_Rate",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(height=360, margin=dict(l=10,r=10,t=55,b=10), yaxis_range=[0, max(40, overtime["Attrition_Rate"].max()*1.2)])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col4:
        fig = px.bar(
            tenure, x="Tenure_Band", y="Attrition_Rate",
            title="Attrition by tenure at company",
            labels={"Attrition_Rate": "Attrition rate (%)", "Tenure_Band": "Years at company"},
            text="Attrition_Rate",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(height=360, margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    col5, col6 = st.columns(2)
    with col5:
        fig = px.box(
            filtered, x="Attrition", y="MonthlyIncome", points=False,
            title="Monthly income by attrition status",
            labels={"MonthlyIncome": "Monthly income ($)", "Attrition": "Attrition"},
        )
        fig.update_layout(height=390, margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col6:
        sat = (
            filtered.groupby("JobSatisfaction", as_index=False)["Attrition_Flag"]
            .mean()
            .assign(Attrition_Rate=lambda x: x["Attrition_Flag"] * 100)
        )
        fig = px.bar(
            sat, x="JobSatisfaction", y="Attrition_Rate",
            title="Attrition by job satisfaction",
            labels={"Attrition_Rate": "Attrition rate (%)", "JobSatisfaction": "Job satisfaction (1–4)"},
            text="Attrition_Rate",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(height=390, margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Statistical evidence
    st.markdown('<div class="section-title">Statistical evidence</div>', unsafe_allow_html=True)
    ct = pd.crosstab(filtered["OverTime"], filtered["Attrition"])
    if ct.shape == (2, 2):
        chi2, p_chi, _, _ = chi2_contingency(ct)
    else:
        chi2, p_chi = np.nan, np.nan

    income_left = filtered.loc[filtered["Attrition_Flag"] == 1, "MonthlyIncome"]
    income_stay = filtered.loc[filtered["Attrition_Flag"] == 0, "MonthlyIncome"]
    if len(income_left) > 1 and len(income_stay) > 1:
        _, p_income = ttest_ind(income_left, income_stay, equal_var=False)
    else:
        p_income = np.nan

    s1, s2 = st.columns(2)
    with s1:
        ptxt = f"{p_chi:.2e}" if pd.notna(p_chi) else "N/A"
        st.markdown(
            f'<div class="insight"><b>Overtime × Attrition — chi-square test</b><br>'
            f'p-value: <b>{ptxt}</b><br>'
            f'<span class="muted">A very small p-value indicates a statistically significant association in the selected population. '
            f'It does not prove that overtime causes attrition.</span></div>',
            unsafe_allow_html=True,
        )
    with s2:
        ptxt = f"{p_income:.2e}" if pd.notna(p_income) else "N/A"
        st.markdown(
            f'<div class="insight"><b>Monthly income × Attrition — Welch t-test</b><br>'
            f'p-value: <b>{ptxt}</b><br>'
            f'<span class="muted">Tests whether mean monthly income differs between employees who left and stayed.</span></div>',
            unsafe_allow_html=True,
        )

    # Business insights
    st.markdown('<div class="section-title">Business insights & recommendations</div>', unsafe_allow_html=True)

    role_full = role.sort_values("Attrition_Rate", ascending=False)
    top_role = role_full.iloc[0]
    overtime_map = overtime.set_index("OverTime")["Attrition_Rate"].to_dict()
    overtime_max = max(overtime_map, key=overtime_map.get)
    overtime_min = min(overtime_map, key=overtime_map.get)
    overtime_ratio = (
        overtime_map[overtime_max] / overtime_map[overtime_min]
        if overtime_map.get(overtime_min, 0) else np.nan
    )

    i1, i2, i3 = st.columns(3)
    i1.markdown(
        f'<div class="insight"><b>Highest-risk role</b><br>'
        f'{top_role["JobRole"]}: {top_role["Attrition_Rate"]:.1f}% attrition among {int(top_role["Employees"]):,} employees.</div>',
        unsafe_allow_html=True,
    )
    i2.markdown(
        f'<div class="insight"><b>Overtime signal</b><br>'
        f'{overtime_max} overtime group shows {overtime_map[overtime_max]:.1f}% attrition vs '
        f'{overtime_map[overtime_min]:.1f}% for {overtime_min}.</div>',
        unsafe_allow_html=True,
    )
    i3.markdown(
        f'<div class="insight"><b>Retention priority</b><br>'
        f'Prioritize early-tenure employees, high-risk roles and teams with sustained overtime exposure.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="note"><b>Analytical caveat:</b> This is observational employee data. '
        'Statistical significance indicates association, not causation. Recommendations should be validated with '
        'additional HR context and longitudinal data.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="muted">Dataset: IBM HR Analytics Employee Attrition & Performance. '
        'All figures update with the selected filters.</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
