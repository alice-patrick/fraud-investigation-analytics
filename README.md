# 🚨 Fraud Investigation Analytics

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

---

## Overview

Fraud Investigation Analytics is an operational fraud monitoring platform built on SQL investigation reports and an interactive Streamlit dashboard.

Unlike machine learning model repositories that focus on prediction, this project focuses on **fraud operations**, enabling analysts to investigate high-risk accounts, monitor suspicious transaction behaviour, prioritize investigations, and evaluate operational fraud exposure.

This repository demonstrates how SQL investigation queries can be transformed into decision-support dashboards for fraud analysts.

---

## Relationship to the Main Project

This repository is part of the **Adaptive Fraud Intelligence** ecosystem.

**Main Repository**

https://github.com/alice-patrick/adaptive-fraud-intelligence

The main project performs fraud prediction and adaptive decision-making.

This repository focuses on the operational investigation layer built on top of those decision outputs.

---

# Dashboard Features

- Operational Risk Monitoring
- High Risk Account Investigation
- High Velocity Transaction Detection
- Repeated Destination Account Analysis
- Cross-Border Fraud Monitoring
- Interactive Investigation Drill-Down
- Downloadable Investigation Reports
- SQL-powered Fraud Analytics
- Operational KPIs
- Interactive Plotly Visualizations

---

# Dashboard Overview

The main operational dashboard summarizes fraud alerts, confirmed frauds, fraud conversion rate, expected operational benefit, and investigation workload.

![Dashboard Overview](images/dashboard_overview.png)

---

## Operational Risk Analytics

Interactive visualizations of fraud severity, operational risk concentration, and expected financial benefit.

![Operational Risk Analytics](images/operational_risk_analytics.png)

---

## High Risk Accounts

Identify customer accounts with the highest fraud exposure using operational fraud metrics.

![High Risk Accounts](images/high_risk_accounts.png)

---

## Expected Exposure Ranking

Rank customer accounts by expected financial loss and investigation priority.

![Expected Exposure Ranking](images/expected_exposure_ranking.png)

---

## Account Investigation Drill-Down

Investigate a customer by combining information from multiple SQL investigation reports into a unified operational view.

![Account Investigation Drill-Down](images/account_investigation_drilldown.png)

---

## High Velocity Transactions

Detect burst transaction behaviour and suspicious account activity occurring within short time windows.

![High Velocity Transactions](images/high_velocity_transactions.png)

---

## Velocity Analytics

Analyze high-velocity accounts ranked by expected fraud exposure.

![Velocity Analytics](images/velocity_analytics.png)

---

## Repeated Destination Accounts

Identify destination accounts repeatedly receiving suspicious transfers from multiple customers.

![Repeated Destination Accounts](images/repeated_destination_accounts.png)

---

## Destination Risk Analytics

Rank destination accounts using a composite destination risk index and expected fraud exposure.

![Destination Risk Analytics](images/destination_risk_analytics.png)

---

## Cross-Border Alerts

Monitor geographically distributed fraud activity using country, channel, device, fraud score, and expected loss indicators.

![Cross-Border Alerts](images/cross_border_alerts.png)

---

## Cross-Border Risk Analytics

Visualize country-level fraud exposure and combined cross-border risk signals.

![Cross-Border Risk Analytics](images/cross-border_risk_analytics.png)

---

# Project Structure

```text
fraud-investigation-analytics/
│
├── dashboards/
│   └── fraud_operations_monitoring.py
│
├── sql/
│   ├── top_operational_risks.sql
│   ├── high_risk_accounts.sql
│   ├── high_velocity_transactions.sql
│   ├── repeated_destination_accounts.sql
│   ├── cross_border_alerts.sql
│   ├── precision_recall_at_k.sql
│   ├── operational_cost_performance.sql
│   └── model_decision_performance.sql
│
├── reports/
│
├── scripts/
│   └── run_sql_report.py
│
├── images/
│
├── requirements.txt
│
└── README.md
```

---

# Technology Stack

- Python
- SQL
- SQLite
- Streamlit
- Plotly
- Pandas

---

# Installation

Clone the repository

```bash
git clone https://github.com/alice-patrick/fraud-investigation-analytics.git
```

Move into the project

```bash
cd fraud-investigation-analytics
```

Install dependencies

```bash
pip install -r requirements.txt
```

Launch the dashboard

```bash
streamlit run dashboards/fraud_operations_monitoring.py
```

---

# Project Goals

This project demonstrates how SQL investigation reports can be transformed into a fraud operations dashboard capable of supporting analyst decision-making through interactive visual analytics.

Key objectives include:

- Fraud investigation prioritization
- Operational fraud monitoring
- Investigation workflow support
- Fraud exposure analysis
- SQL-based reporting
- Decision support analytics

---

# Author

**ALIKI Pipitsa**

MSc Artificial Intelligence

University of Essex

---

## License

MIT License
