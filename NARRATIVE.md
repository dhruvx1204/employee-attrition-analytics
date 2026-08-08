# Employee Attrition Analysis — Findings & Recommendations

*(Real dataset: IBM HR Analytics Employee Attrition, Kaggle — 1,470
employees, overall attrition rate 16.1%)*

## 1. Business Question
What is driving employee attrition at this company, and which
departments/roles are most at risk?

## 2. Key Findings

- **Overtime is the strongest attrition-associated factor.** Employees working
  overtime leave at 30.5% vs 10.4% for those who don't — nearly 3x higher,
  and highly statistically significant (chi-square p < 0.000001).
- **Income is also a significant driver here** (unlike some other
  companies' data) — employees who left earned $4,787/month on average vs
  $6,833 for those who stayed, a large and statistically significant gap
  (Welch's t-test p < 0.000001).
- **Sales has the highest departmental attrition** at 20.6%, followed by
  HR at 19.0%. R&D is lowest at 13.8%.
- **Sales Representative is the single highest-risk job role** at 39.8%
  attrition — more than double the company average. Lab Technician (23.9%)
  and HR (23.1%) are the next highest.
- **Job satisfaction shows a mostly inverse relationship** — attrition
  drops from 22.8% (lowest satisfaction) to 11.3% (highest), though the
  drop isn't perfectly linear (satisfaction levels 2 and 3 are close).
- **Tenure risk decreases steadily and sharply** — 34.9% attrition in
  year 0-1, dropping to just 8.1% for employees with 10+ years. New-hire
  retention is clearly the biggest opportunity, not a U-shaped pattern.

## 3. Recommendations
- **Fix overtime and compensation together for Sales Representatives** —
  this role combines the two strongest risk factors (high overtime
  exposure + lower pay) and has by far the highest attrition rate.
- **Front-load retention efforts into the first year.** Attrition is
  concentrated almost entirely in year 0-1 (34.9%) and falls off sharply
  after — suggests an onboarding/early-fit problem more than a long-term
  engagement problem.
- **Review pay bands for roles with high attrition**, since income is a
  real, statistically significant factor in this dataset (unlike the
  common assumption that money doesn't matter — here it clearly does).

## 4. Methodology Note
- Cleaned dataset: dropped constant columns (EmployeeCount, StandardHours,
  Over18) that carried no analytical information.
- Used chi-square test for the categorical relationship (OverTime vs
  Attrition) and Welch's t-test for the continuous relationship (Income vs
  Attrition) to confirm findings weren't due to random noise — both came
  back highly significant (p < 0.000001).
- Also broke down attrition by JobRole as a follow-up cut, since
  "which department" is often too coarse a question in interviews.

## 5. How to present this on your resume
"Analyzed IBM HR dataset (1,470 employees) to identify attrition drivers;
found overtime (30.5% vs 10.4% attrition) and income both statistically
significant (p<0.000001), with Sales Representatives at 39.8% attrition —
delivered 3 actionable retention recommendations via Python
(pandas/scipy/Plotly)."


## Statistical interpretation note

This analysis uses observational data. Significant tests indicate association, not causation. Overtime and income should therefore be described as factors associated with attrition rather than proven causes.
